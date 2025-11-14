"""
Huffman Coding Algorithm Routes
Handles all Huffman compression operations
"""

from flask import Blueprint, request, jsonify
import sys
import os
import time
import pickle
import re
import unicodedata
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from algorithms import huffman
from handlers import image_handler, video_handler, document_handler
from utils.database import CompressionDB, get_db

huffman_bp = Blueprint('huffman', __name__, url_prefix='/huffman')

def sanitize_filename(filename):
    """Sanitize filename to remove special characters and make it filesystem-safe"""
    # Normalize unicode characters
    filename = unicodedata.normalize('NFKD', filename)
    # Remove non-ASCII characters
    filename = filename.encode('ASCII', 'ignore').decode('ASCII')
    # Replace spaces and special chars with underscores
    filename = re.sub(r'[^\w\s.-]', '_', filename)
    # Replace multiple spaces/underscores with single underscore
    filename = re.sub(r'[\s_]+', '_', filename)
    # Remove leading/trailing underscores and dots
    filename = filename.strip('_.')
    # Ensure filename is not empty
    if not filename:
        filename = 'unnamed_file'
    return filename

# Initialize database
db = CompressionDB()


@huffman_bp.route('/compress/text', methods=['POST'])
def compress_text():
    """Compress text using Huffman algorithm"""
    try:
        data = request.json
        text = data.get('text', '')
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        # Store original file in database
        original_file_id = db.store_file(
            file_data=text.encode(),
            filename='text_input.txt',
            file_type='text/plain'
        )
        
        # Measure compression time
        start_time = time.time()
        encoded, codes = huffman.compress(text)
        compress_time = time.time() - start_time
        
        # Measure decompression time
        start_time = time.time()
        decoded_list = huffman.decompress(encoded, codes)
        decoded = ''.join(decoded_list) if isinstance(decoded_list, list) else decoded_list
        decompress_time = time.time() - start_time
        
        # Calculate metrics
        original_size = len(text.encode())
        compressed_size = len(encoded) // 8 + (1 if len(encoded) % 8 else 0)
        ratio = compressed_size / original_size if original_size > 0 else 0
        savings = ((original_size - compressed_size) / original_size * 100) if original_size > 0 else 0
        
        # Verify correctness
        is_correct = text == decoded
        
        # Store compressed data
        compressed_file_id = db.store_compressed_file(
            compressed_data=encoded.encode() if isinstance(encoded, str) else str(encoded).encode(),
            filename='text_input.txt',
            algorithm='Huffman'
        )
        
        # Save compression record
        record = {
            'filename': 'text_input.txt',
            'file_type': 'text',
            'algorithm': 'Huffman',
            'original_size': original_size,
            'compressed_size': compressed_size,
            'compression_ratio': ratio,
            'space_savings': savings,
            'compression_time': compress_time,
            'decompression_time': decompress_time,
            'original_file_id': original_file_id,
            'compressed_file_id': compressed_file_id
        }
        record_id = db.save_compression_record(record)
        
        return jsonify({
            'algorithm': 'Huffman',
            'original_size': original_size,
            'compressed_size': compressed_size,
            'compression_ratio': round(ratio, 4),
            'space_savings': round(savings, 2),
            'compression_time': round(compress_time, 6),
            'decompression_time': round(decompress_time, 6),
            'is_correct': is_correct,
            'decompressed_text': decoded if is_correct else '',
            'record_id': str(record_id),
            'original_file_id': str(original_file_id),
            'compressed_file_id': str(compressed_file_id)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@huffman_bp.route('/compress/image', methods=['POST'])
def compress_image():
    """Compress image using Huffman algorithm"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        grayscale = request.form.get('grayscale', 'false').lower() == 'true'
        resize_percent = request.form.get('resize')
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Sanitize filename
        safe_filename = sanitize_filename(file.filename)
        
        # Save uploaded file
        upload_folder = os.path.join(os.path.dirname(__file__), '..', 'uploads')
        os.makedirs(upload_folder, exist_ok=True)
        filepath = os.path.join(upload_folder, safe_filename)
        file.save(filepath)
        
        # Process image with optional resize
        resize_param = int(resize_percent) if resize_percent and resize_percent != 'none' else None
        image_data = image_handler.prepare_for_compression(
            filepath, 
            grayscale=grayscale,
            resize_percent=resize_param
        )
        data = image_data['data']
        
        # Convert to text for Huffman
        text = ''.join(chr(min(d, 255)) for d in data)
        
        # Compress
        start_time = time.time()
        encoded, codes = huffman.compress(text)
        compress_time = time.time() - start_time
        
        # Decompress
        start_time = time.time()
        decoded = huffman.decompress(encoded, codes)
        decompress_time = time.time() - start_time
        
        # Calculate metrics - Huffman compressed size estimation
        original_size = len(data)
        # Huffman: encoded bits + code table
        # Encoded size in bytes + code table size (roughly 256 * 4 bytes for typical case)
        encoded_bytes = len(encoded) // 8 + (1 if len(encoded) % 8 else 0)
        code_table_bytes = len(codes) * 4  # Rough estimate: 4 bytes per code entry
        compressed_size = encoded_bytes + code_table_bytes
        ratio = compressed_size / original_size if original_size > 0 else 0
        savings = ((original_size - compressed_size) / original_size * 100) if original_size > 0 else 0
        
        # Fix: decompress returns a list, convert to string for comparison
        decoded_text = ''.join(decoded) if isinstance(decoded, list) else decoded
        is_correct = text == decoded_text
        
        # Store in database
        db = get_db()
        
        # Store original file
        with open(filepath, 'rb') as f:
            original_bytes = f.read()
        original_file_id = db.store_file(original_bytes, file.filename, 'image')
        
        # Store compressed data with metadata for reconstruction
        compressed_data = {
            'encoded': encoded,
            'codes': codes,
            'shape': image_data.get('shape'),
            'mode': image_data.get('mode'),
            'format': image_data.get('format')
        }
        compressed_bytes = pickle.dumps(compressed_data)
        compressed_file_id = db.store_compressed_file(compressed_bytes, file.filename, 'huffman')
        
        # Calculate ACTUAL file size (including pickle overhead for download)
        actual_compressed_size = len(compressed_bytes)
        actual_ratio = actual_compressed_size / original_size if original_size > 0 else 0
        actual_savings = ((original_size - actual_compressed_size) / original_size * 100) if original_size > 0 else 0
        
        # Save compression record
        record = {
            'filename': file.filename,
            'file_type': 'image',
            'algorithm': 'Huffman',
            'original_size': original_size,
            'compressed_size': compressed_size,
            'compression_ratio': ratio,
            'space_savings': savings,
            'compression_time': compress_time,
            'decompression_time': decompress_time,
            'is_correct': is_correct,
            'original_file_id': original_file_id,
            'compressed_file_id': compressed_file_id,
            'actual_file_size': actual_compressed_size,
            'actual_ratio': round(actual_ratio, 4),
            'actual_savings': round(actual_savings, 2),
        }
        record_id = db.save_compression_record(record)
        
        # Cleanup
        os.remove(filepath)
        
        return jsonify({
            'algorithm': 'Huffman',
            'file_type': 'image',
            'original_size': original_size,
            'compressed_size': compressed_size,
            'compression_ratio': round(ratio, 4),
            'space_savings': round(savings, 2),
            'actual_file_size': actual_compressed_size,
            'actual_ratio': round(actual_ratio, 4),
            'actual_savings': round(actual_savings, 2),
            'compression_time': round(compress_time, 6),
            'decompression_time': round(decompress_time, 6),
            'is_correct': is_correct,
            'record_id': record_id,
            'original_file_id': original_file_id,
            'compressed_file_id': compressed_file_id,
            'metadata': {
                'shape': image_data.get('shape'),
                'mode': image_data.get('mode'),
                'format': image_data.get('format'),
                'grayscale': grayscale
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@huffman_bp.route('/compress/video', methods=['POST'])
def compress_video():
    """Compress video using Huffman algorithm"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        grayscale = request.form.get('grayscale', 'false').lower() == 'true'
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Sanitize filename
        safe_filename = sanitize_filename(file.filename)
        
        # Save uploaded file
        upload_folder = os.path.join(os.path.dirname(__file__), '..', 'uploads')
        os.makedirs(upload_folder, exist_ok=True)
        filepath = os.path.join(upload_folder, safe_filename)
        file.save(filepath)
        
        # Process video (first frame only for demo)
        video_data = video_handler.prepare_for_compression(filepath, grayscale=grayscale, max_frames=1)
        data = video_data['data'][0] if video_data['data'] else []
        
        # Convert to text for Huffman
        text = ''.join(chr(min(d, 255)) for d in data)
        
        # Compress
        start_time = time.time()
        encoded, codes = huffman.compress(text)
        compress_time = time.time() - start_time
        
        # Decompress
        start_time = time.time()
        decoded = huffman.decompress(encoded, codes)
        decompress_time = time.time() - start_time
        
        # Calculate metrics
        original_size = len(data)
        compressed_size = len(encoded) // 8 + (1 if len(encoded) % 8 else 0)
        ratio = compressed_size / original_size if original_size > 0 else 0
        savings = ((original_size - compressed_size) / original_size * 100) if original_size > 0 else 0
        is_correct = text == decoded
        
        # Store in database
        db = get_db()
        
        # Store original file
        with open(filepath, 'rb') as f:
            original_bytes = f.read()
        original_file_id = db.store_file(original_bytes, file.filename, 'video')
        
        # Store compressed data with metadata for reconstruction
        compressed_data = {
            'encoded': encoded,
            'codes': codes,
            'fps': video_data.get('fps'),
            'width': video_data.get('width'),
            'height': video_data.get('height'),
            'frame_count': video_data.get('frame_count')
        }
        compressed_bytes = pickle.dumps(compressed_data)
        compressed_file_id = db.store_compressed_file(compressed_bytes, file.filename, 'huffman')
        
        # Save compression record
        record = {
            'filename': file.filename,
            'file_type': 'video',
            'algorithm': 'Huffman',
            'original_size': original_size,
            'compressed_size': compressed_size,
            'compression_ratio': ratio,
            'space_savings': savings,
            'compression_time': compress_time,
            'decompression_time': decompress_time,
            'is_correct': is_correct,
            'original_file_id': original_file_id,
            'compressed_file_id': compressed_file_id,
            'metadata': {
                'fps': video_data.get('fps'),
                'width': video_data.get('width'),
                'height': video_data.get('height'),
                'frame_count': video_data.get('frame_count'),
                'grayscale': grayscale
            }
        }
        record_id = db.save_compression_record(record)
        
        # Cleanup
        os.remove(filepath)
        
        return jsonify({
            'record_id': record_id,
            'original_file_id': original_file_id,
            'compressed_file_id': compressed_file_id,
            'algorithm': 'Huffman',
            'file_type': 'video',
            'original_size': original_size,
            'compressed_size': compressed_size,
            'compression_ratio': round(ratio, 4),
            'space_savings': round(savings, 2),
            'compression_time': round(compress_time, 6),
            'decompression_time': round(decompress_time, 6),
            'is_correct': is_correct,
            'metadata': {
                'fps': video_data.get('fps'),
                'width': video_data.get('width'),
                'height': video_data.get('height'),
                'frame_count': video_data.get('frame_count'),
                'grayscale': grayscale
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@huffman_bp.route('/compress/document', methods=['POST'])
def compress_document():
    """Compress document using Huffman algorithm"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Sanitize filename
        safe_filename = sanitize_filename(file.filename)
        
        # Save uploaded file
        upload_folder = os.path.join(os.path.dirname(__file__), '..', 'uploads')
        os.makedirs(upload_folder, exist_ok=True)
        filepath = os.path.join(upload_folder, safe_filename)
        file.save(filepath)
        
        # Process document
        doc_data = document_handler.prepare_for_compression(filepath)
        content = doc_data['data']
        data = [ord(c) for c in content]
        
        # Convert to text for Huffman
        text = ''.join(chr(min(d, 255)) for d in data)
        
        # Compress
        start_time = time.time()
        encoded, codes = huffman.compress(text)
        compress_time = time.time() - start_time
        
        # Decompress
        start_time = time.time()
        decoded = huffman.decompress(encoded, codes)
        decompress_time = time.time() - start_time
        
        # Calculate metrics
        original_size = len(data)
        compressed_size = len(encoded) // 8 + (1 if len(encoded) % 8 else 0)
        ratio = compressed_size / original_size if original_size > 0 else 0
        savings = ((original_size - compressed_size) / original_size * 100) if original_size > 0 else 0
        is_correct = text == decoded
        
        # Store in database
        db = get_db()
        
        # Store original file
        with open(filepath, 'rb') as f:
            original_bytes = f.read()
        original_file_id = db.store_file(original_bytes, file.filename, 'document')
        
        # Store compressed data with metadata
        compressed_data = {
            'encoded': encoded,
            'codes': codes,
            'format': doc_data.get('format'),
            'length': doc_data.get('length')
        }
        compressed_bytes = pickle.dumps(compressed_data)
        compressed_file_id = db.store_compressed_file(compressed_bytes, file.filename, 'huffman')
        
        # Save compression record
        record = {
            'filename': file.filename,
            'file_type': 'document',
            'algorithm': 'Huffman',
            'original_size': original_size,
            'compressed_size': compressed_size,
            'compression_ratio': ratio,
            'space_savings': savings,
            'compression_time': compress_time,
            'decompression_time': decompress_time,
            'is_correct': is_correct,
            'original_file_id': original_file_id,
            'compressed_file_id': compressed_file_id,
            'metadata': {
                'format': doc_data.get('format'),
                'length': doc_data.get('length')
            }
        }
        record_id = db.save_compression_record(record)
        
        # Cleanup
        os.remove(filepath)
        
        return jsonify({
            'record_id': record_id,
            'original_file_id': original_file_id,
            'compressed_file_id': compressed_file_id,
            'algorithm': 'Huffman',
            'file_type': 'document',
            'original_size': original_size,
            'compressed_size': compressed_size,
            'compression_ratio': round(ratio, 4),
            'space_savings': round(savings, 2),
            'compression_time': round(compress_time, 6),
            'decompression_time': round(decompress_time, 6),
            'is_correct': is_correct,
            'metadata': {
                'format': doc_data.get('format'),
                'length': doc_data.get('length')
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
