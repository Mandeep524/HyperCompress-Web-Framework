"""
Web-based User Interface for Data Compression Project
Run with: python web_ui.py
Then open: http://localhost:5000
"""

from flask import Flask, render_template, request, jsonify
import sys
import os
import time
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from algorithms import rle, huffman, lzw
from handlers import image_handler, video_handler, document_handler

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'

# Create uploads directory
os.makedirs('uploads', exist_ok=True)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Data Compression Project</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        .header p {
            font-size: 1.1em;
            opacity: 0.9;
        }
        
        .content {
            padding: 30px;
        }
        
        .section {
            margin-bottom: 30px;
        }
        
        .section-title {
            font-size: 1.3em;
            color: #667eea;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 2px solid #f0f0f0;
        }
        
        textarea {
            width: 100%;
            padding: 15px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-family: 'Courier New', monospace;
            font-size: 14px;
            resize: vertical;
            transition: border-color 0.3s;
        }
        
        textarea:focus {
            outline: none;
            border-color: #667eea;
        }
        
        .algorithm-options {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }
        
        .algorithm-card {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s;
            border: 2px solid transparent;
        }
        
        .algorithm-card:hover {
            background: #e9ecef;
            transform: translateY(-2px);
        }
        
        .algorithm-card.selected {
            border-color: #667eea;
            background: #e7eaf6;
        }
        
        .algorithm-card input[type="radio"] {
            margin-right: 10px;
        }
        
        .algorithm-title {
            font-weight: bold;
            color: #333;
            margin-bottom: 5px;
        }
        
        .algorithm-desc {
            font-size: 0.85em;
            color: #666;
        }
        
        .btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px 40px;
            border: none;
            border-radius: 8px;
            font-size: 1.1em;
            font-weight: bold;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
            margin: 10px 5px;
        }
        
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
        }
        
        .btn:active {
            transform: translateY(0);
        }
        
        .btn-secondary {
            background: #6c757d;
        }
        
        #loading {
            display: none;
            text-align: center;
            padding: 20px;
        }
        
        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto 15px;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        #results {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            display: none;
            margin-top: 20px;
        }
        
        .result-card {
            background: white;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 15px;
            border-left: 4px solid #667eea;
        }
        
        .result-header {
            font-size: 1.2em;
            font-weight: bold;
            color: #333;
            margin-bottom: 15px;
        }
        
        .result-row {
            display: flex;
            justify-content: space-between;
            padding: 8px 0;
            border-bottom: 1px solid #f0f0f0;
        }
        
        .result-label {
            color: #666;
        }
        
        .result-value {
            font-weight: bold;
            color: #333;
        }
        
        .success {
            color: #27ae60;
        }
        
        .warning {
            color: #f39c12;
        }
        
        .error {
            color: #e74c3c;
        }
        
        .summary {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 8px;
            margin-top: 20px;
        }
        
        .summary h3 {
            margin-bottom: 15px;
        }
        
        .summary-item {
            padding: 8px 0;
            font-size: 1.05em;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🗜️ Data Compression Project</h1>
            <p>Compare RLE, Huffman, and LZW Algorithms</p>
        </div>
        
        <div class="content">
            <div class="section">
                <div class="section-title">� Upload File (Images/Videos/Documents)</div>
                <div style="margin-bottom: 20px;">
                    <input type="file" id="fileInput" accept=".png,.jpg,.jpeg,.bmp,.gif,.mp4,.avi,.mov,.txt,.pdf,.docx,.csv" style="display: none;" onchange="handleFileSelect(event)">
                    <button class="btn btn-secondary" onclick="document.getElementById('fileInput').click()">
                        📤 Choose File
                    </button>
                    <span id="fileName" style="margin-left: 15px; color: #666;"></span>
                </div>
                <div style="background: #f0f0f0; padding: 15px; border-radius: 8px; margin-top: 10px;">
                    <strong>Supported formats:</strong><br>
                    • Images: PNG, JPG, JPEG, BMP, GIF<br>
                    • Videos: MP4, AVI, MOV<br>
                    • Documents: TXT, PDF, DOCX, CSV
                </div>
            </div>
            
            <div class="section">
                <div class="section-title">�📝 Or Enter Text to Compress</div>
                <textarea id="textInput" rows="8" placeholder="Type or paste your text here...
Example: AAAABBBBCCCCDDDD (repetitive)
Example: The quick brown fox jumps over the lazy dog (natural text)"></textarea>
            </div>
            
            <div class="section">
                <div class="section-title">⚙️ Select Algorithm</div>
                <div class="algorithm-options">
                    <div class="algorithm-card selected" onclick="selectAlgorithm('all')">
                        <input type="radio" name="algorithm" value="all" checked>
                        <div class="algorithm-title">All Algorithms</div>
                        <div class="algorithm-desc">Compare all three</div>
                    </div>
                    <div class="algorithm-card" onclick="selectAlgorithm('rle')">
                        <input type="radio" name="algorithm" value="rle">
                        <div class="algorithm-title">RLE</div>
                        <div class="algorithm-desc">Best for repetitive data</div>
                    </div>
                    <div class="algorithm-card" onclick="selectAlgorithm('huffman')">
                        <input type="radio" name="algorithm" value="huffman">
                        <div class="algorithm-title">Huffman</div>
                        <div class="algorithm-desc">Best for text</div>
                    </div>
                    <div class="algorithm-card" onclick="selectAlgorithm('lzw')">
                        <input type="radio" name="algorithm" value="lzw">
                        <div class="algorithm-title">LZW</div>
                        <div class="algorithm-desc">Best for patterns</div>
                    </div>
                </div>
            </div>
            
            <div class="section" style="text-align: center;">
                <button class="btn" onclick="compress()">🗜️ Compress & Analyze</button>
                <button class="btn btn-secondary" onclick="clearResults()">🗑️ Clear</button>
            </div>
            
            <div id="loading">
                <div class="spinner"></div>
                <p>Compressing...</p>
            </div>
            
            <div id="results"></div>
        </div>
    </div>
    
    <script>
        let selectedFile = null;
        
        function handleFileSelect(event) {
            selectedFile = event.target.files[0];
            if (selectedFile) {
                document.getElementById('fileName').textContent = `Selected: ${selectedFile.name} (${formatBytes(selectedFile.size)})`;
                document.getElementById('textInput').value = ''; // Clear text input
            }
        }
        
        function formatBytes(bytes) {
            if (bytes === 0) return '0 Bytes';
            const k = 1024;
            const sizes = ['Bytes', 'KB', 'MB', 'GB'];
            const i = Math.floor(Math.log(bytes) / Math.log(k));
            return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
        }
        
        function selectAlgorithm(algo) {
            document.querySelectorAll('.algorithm-card').forEach(card => {
                card.classList.remove('selected');
            });
            event.currentTarget.classList.add('selected');
            document.querySelector(`input[value="${algo}"]`).checked = true;
        }
        
        async function compress() {
            const text = document.getElementById('textInput').value.trim();
            const algorithm = document.querySelector('input[name="algorithm"]:checked').value;
            
            // Check if we have file or text
            if (!selectedFile && !text) {
                alert('Please upload a file or enter text to compress!');
                return;
            }
            
            document.getElementById('loading').style.display = 'block';
            document.getElementById('results').style.display = 'none';
            
            try {
                let response;
                
                if (selectedFile) {
                    // File upload
                    const formData = new FormData();
                    formData.append('file', selectedFile);
                    formData.append('algorithm', algorithm);
                    
                    response = await fetch('/compress_file', {
                        method: 'POST',
                        body: formData
                    });
                } else {
                    // Text compression
                    response = await fetch('/compress', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ text, algorithm })
                    });
                }
                
                const data = await response.json();
                
                if (data.error) {
                    alert('Error: ' + data.error);
                } else {
                    displayResults(data);
                }
            } catch (error) {
                alert('Error: ' + error.message);
            } finally {
                document.getElementById('loading').style.display = 'none';
            }
        }
        
        function displayResults(data) {
            const resultsDiv = document.getElementById('results');
            let html = '<h2 style="margin-bottom: 20px;">📊 Compression Results</h2>';
            
            data.results.forEach(result => {
                const savingClass = result.space_saving >= 0 ? 'success' : 'warning';
                const savingText = result.space_saving >= 0 
                    ? `${result.space_saving.toFixed(2)}% Saved` 
                    : `${Math.abs(result.space_saving).toFixed(2)}% Expanded`;
                
                html += `
                    <div class="result-card">
                        <div class="result-header">${result.algorithm}</div>
                        <div class="result-row">
                            <span class="result-label">Original Size:</span>
                            <span class="result-value">${result.original_size.toLocaleString()} bytes</span>
                        </div>
                        <div class="result-row">
                            <span class="result-label">Compressed Size:</span>
                            <span class="result-value">${result.compressed_size.toLocaleString()} bytes</span>
                        </div>
                        <div class="result-row">
                            <span class="result-label">Compression Ratio:</span>
                            <span class="result-value">${result.compression_ratio.toFixed(4)}</span>
                        </div>
                        <div class="result-row">
                            <span class="result-label">Space Savings:</span>
                            <span class="result-value ${savingClass}">${savingText}</span>
                        </div>
                        <div class="result-row">
                            <span class="result-label">Compression Time:</span>
                            <span class="result-value">${result.compression_time.toFixed(6)}s</span>
                        </div>
                        <div class="result-row">
                            <span class="result-label">Decompression Time:</span>
                            <span class="result-value">${result.decompression_time.toFixed(6)}s</span>
                        </div>
                        <div class="result-row">
                            <span class="result-label">Verification:</span>
                            <span class="result-value success">${result.correct ? '✓ PASSED' : '✗ FAILED'}</span>
                        </div>
                    </div>
                `;
            });
            
            if (data.summary) {
                html += `
                    <div class="summary">
                        <h3>🏆 Best Performers</h3>
                        ${data.summary.best_compression ? 
                            `<div class="summary-item">📦 Best Compression: <strong>${data.summary.best_compression.name}</strong> (${data.summary.best_compression.saving.toFixed(2)}% saved)</div>` :
                            `<div class="summary-item">⚠️ No algorithm achieved compression</div>`
                        }
                        <div class="summary-item">⚡ Fastest Compression: <strong>${data.summary.fastest_comp.name}</strong> (${data.summary.fastest_comp.time.toFixed(6)}s)</div>
                        <div class="summary-item">🔄 Fastest Decompression: <strong>${data.summary.fastest_decomp.name}</strong> (${data.summary.fastest_decomp.time.toFixed(6)}s)</div>
                    </div>
                `;
            }
            
            resultsDiv.innerHTML = html;
            resultsDiv.style.display = 'block';
            resultsDiv.scrollIntoView({ behavior: 'smooth' });
        }
        
        function clearResults() {
            document.getElementById('textInput').value = '';
            document.getElementById('fileInput').value = '';
            document.getElementById('fileName').textContent = '';
            document.getElementById('results').style.display = 'none';
            selectedFile = null;
        }
        
        // Load sample text on page load
        window.addEventListener('load', () => {
            document.getElementById('textInput').value = 'AAAABBBBCCCCDDDDEEEEFFFFGGGG'.repeat(20);
        });
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return HTML_TEMPLATE

@app.route('/compress_file', methods=['POST'])
def compress_file():
    """Handle file upload and compression."""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'})
        
        file = request.files['file']
        algorithm = request.form.get('algorithm', 'all')
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'})
        
        # Save uploaded file
        filename = file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Detect file type and load data
        ext = os.path.splitext(filename)[1].lower()
        
        try:
            if ext in ['.png', '.jpg', '.jpeg', '.bmp', '.gif']:
                # Image file
                img_array = image_handler.load_image(filepath)
                data_list = image_handler.prepare_for_compression(img_array, grayscale=True)
                file_type = 'Image'
                
            elif ext in ['.mp4', '.avi', '.mov']:
                # Video file
                frames = video_handler.load_video(filepath, max_frames=10)
                data_list = video_handler.prepare_for_compression(frames, grayscale=True)
                file_type = 'Video (10 frames)'
                
            elif ext in ['.txt', '.csv']:
                # Text file
                text = document_handler.load_text_file(filepath)
                data_list = [ord(c) for c in text]
                file_type = 'Text Document'
                
            elif ext == '.pdf':
                # PDF file
                text = document_handler.load_pdf(filepath)
                data_list = [ord(c) for c in text]
                file_type = 'PDF Document'
                
            elif ext == '.docx':
                # DOCX file
                text = document_handler.load_docx(filepath)
                data_list = [ord(c) for c in text]
                file_type = 'DOCX Document'
                
            else:
                # Try as text
                with open(filepath, 'rb') as f:
                    data_bytes = f.read()
                data_list = list(data_bytes)
                file_type = 'Binary File'
            
            # Run compression algorithms
            results = []
            
            if algorithm in ['all', 'rle']:
                result = test_algorithm('RLE', rle.compress, rle.decompress, data_list, None, is_rle=True)
                result['file_type'] = file_type
                results.append(result)
            
            if algorithm in ['all', 'huffman']:
                result = test_algorithm('Huffman', huffman.compress, huffman.decompress, data_list, None, is_huffman=True)
                result['file_type'] = file_type
                results.append(result)
            
            if algorithm in ['all', 'lzw']:
                result = test_algorithm('LZW', lzw.compress, lzw.decompress, data_list, None)
                result['file_type'] = file_type
                results.append(result)
            
            # Generate summary
            summary = generate_summary(results)
            
            return jsonify({
                'results': results,
                'summary': summary,
                'filename': filename,
                'file_type': file_type
            })
            
        finally:
            # Clean up uploaded file
            if os.path.exists(filepath):
                os.remove(filepath)
        
    except Exception as e:
        import traceback
        return jsonify({'error': f'{str(e)}\n{traceback.format_exc()}'})

@app.route('/compress', methods=['POST'])
def compress():
    try:
        data = request.json
        text = data.get('text', '')
        algorithm = data.get('algorithm', 'all')
        
        if not text:
            return jsonify({'error': 'No text provided'})
        
        data_list = [ord(c) for c in text]
        results = []
        
        # Run selected algorithms
        if algorithm in ['all', 'rle']:
            result = test_algorithm('RLE', rle.compress, rle.decompress, data_list, text, is_rle=True)
            results.append(result)
        
        if algorithm in ['all', 'huffman']:
            result = test_algorithm('Huffman', huffman.compress, huffman.decompress, data_list, text, is_huffman=True)
            results.append(result)
        
        if algorithm in ['all', 'lzw']:
            result = test_algorithm('LZW', lzw.compress, lzw.decompress, data_list, text)
            results.append(result)
        
        # Generate summary
        summary = generate_summary(results)
        
        return jsonify({
            'results': results,
            'summary': summary
        })
        
    except Exception as e:
        return jsonify({'error': str(e)})

def test_algorithm(name, compress_func, decompress_func, data_list, data_str, is_rle=False, is_huffman=False):
    """Test an algorithm and return results."""
    
    # Choose data format
    test_data = data_list if is_rle else data_str
    
    # Compress
    start = time.time()
    compressed = compress_func(test_data)
    comp_time = time.time() - start
    
    # Get size
    if is_huffman:
        encoded, codes = compressed
        comp_size = len(encoded)
    elif is_rle:
        comp_size = len(compressed) * 2
    else:
        comp_size = len(str(compressed))
    
    # Decompress
    start = time.time()
    if is_huffman:
        decompressed = decompress_func(encoded, codes)
    else:
        decompressed = decompress_func(compressed)
    decomp_time = time.time() - start
    
    # Metrics
    orig_size = len(data_str)
    ratio = comp_size / orig_size if orig_size > 0 else 1
    space_saving = ((orig_size - comp_size) / orig_size * 100) if orig_size > 0 else 0
    
    # Verify
    if is_huffman:
        is_correct = ''.join(decompressed) == data_str
    elif is_rle:
        is_correct = list(decompressed) == data_list
    else:
        is_correct = decompressed == data_str
    
    return {
        'algorithm': name,
        'original_size': orig_size,
        'compressed_size': comp_size,
        'compression_ratio': ratio,
        'space_saving': space_saving,
        'compression_time': comp_time,
        'decompression_time': decomp_time,
        'correct': is_correct
    }

def generate_summary(results):
    """Generate summary of results."""
    valid = [r for r in results if r['space_saving'] > 0]
    
    summary = {}
    
    if valid:
        best = min(valid, key=lambda x: x['compression_ratio'])
        summary['best_compression'] = {
            'name': best['algorithm'],
            'saving': best['space_saving']
        }
    else:
        summary['best_compression'] = None
    
    fastest_comp = min(results, key=lambda x: x['compression_time'])
    summary['fastest_comp'] = {
        'name': fastest_comp['algorithm'],
        'time': fastest_comp['compression_time']
    }
    
    fastest_decomp = min(results, key=lambda x: x['decompression_time'])
    summary['fastest_decomp'] = {
        'name': fastest_decomp['algorithm'],
        'time': fastest_decomp['decompression_time']
    }
    
    return summary

if __name__ == '__main__':
    print("\n" + "="*60)
    print("  🌐 Data Compression Project - Web Interface")
    print("="*60)
    print("\n📱 Starting web server...")
    print("🌍 Open your browser and go to: http://localhost:8080")
    print("⏹️  Press CTRL+C to stop the server\n")
    
    app.run(debug=True, host='0.0.0.0', port=8080)
