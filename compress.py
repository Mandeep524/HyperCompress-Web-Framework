"""
Main Compression Application
Command-line interface for compressing different file types.
"""

import sys
import os
import argparse
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from algorithms import rle, huffman, lzw
from handlers import image_handler, document_handler, video_handler
from utils import performance, visualization


def detect_file_type(file_path):
    """Detect file type based on extension."""
    ext = os.path.splitext(file_path)[1].lower()
    
    image_exts = ['.png', '.jpg', '.jpeg', '.bmp', '.gif']
    video_exts = ['.mp4', '.avi', '.mov', '.mkv']
    doc_exts = ['.txt', '.pdf', '.docx', '.csv', '.md']
    
    if ext in image_exts:
        return 'image'
    elif ext in video_exts:
        return 'video'
    elif ext in doc_exts:
        return 'document'
    else:
        return 'text'


def compress_file(file_path, algorithm='all', grayscale=False, output_dir='output'):
    """
    Compress a file using specified algorithm(s).
    
    Args:
        file_path: Path to file to compress
        algorithm: 'rle', 'huffman', 'lzw', or 'all'
        grayscale: Convert images/videos to grayscale
        output_dir: Directory for output files
    """
    if not os.path.exists(file_path):
        print(f"Error: File not found: {file_path}")
        return
    
    os.makedirs(output_dir, exist_ok=True)
    
    file_type = detect_file_type(file_path)
    print(f"\n{'='*60}")
    print(f"File: {os.path.basename(file_path)}")
    print(f"Type: {file_type}")
    print(f"Original Size: {performance.format_size(os.path.getsize(file_path))}")
    print(f"{'='*60}\n")
    
    # Prepare data based on file type
    try:
        if file_type == 'image':
            print("Loading image...")
            img_data = image_handler.prepare_for_compression(file_path, grayscale)
            data = img_data['data']
            data_str = ''.join([chr(min(255, max(0, int(d)))) for d in data])
            
        elif file_type == 'video':
            print("Loading video (first 100 frames)...")
            vid_data = video_handler.prepare_for_compression(file_path, grayscale, max_frames=100)
            # Flatten all frames
            data = [item for frame in vid_data['data'] for item in frame]
            data_str = ''.join([chr(min(255, max(0, int(d)))) for d in data])
            
        elif file_type == 'document':
            print("Loading document...")
            doc_data = document_handler.prepare_for_compression(file_path)
            data_str = doc_data['data']
            data = [ord(c) for c in data_str]
            
        else:  # text
            print("Loading text file...")
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                data_str = f.read()
            data = [ord(c) for c in data_str]
    
    except Exception as e:
        print(f"Error loading file: {str(e)}")
        return
    
    print(f"Data loaded: {len(data)} elements\n")
    
    # Setup algorithms to test
    algorithms_to_test = []
    
    if algorithm in ['rle', 'all']:
        algorithms_to_test.append(('RLE', rle.compress, rle.decompress, False))
    
    if algorithm in ['huffman', 'all']:
        algorithms_to_test.append(('Huffman', 
                                   lambda d: huffman.compress(data_str),
                                   lambda c: huffman.decompress(c[0], c[1]),
                                   True))
    
    if algorithm in ['lzw', 'all']:
        algorithms_to_test.append(('LZW', lzw.compress, lzw.decompress, False))
    
    # Run comparison
    print("Running compression tests...\n")
    results = performance.compare_algorithms(data, algorithms_to_test)
    
    # Display results
    performance.print_comparison_table(results)
    
    # Save results
    results_file = os.path.join(output_dir, f"{Path(file_path).stem}_results.json")
    performance.save_results(results, results_file)
    
    # Generate visualizations
    print("\nGenerating visualizations...")
    viz_dir = os.path.join(output_dir, f"{Path(file_path).stem}_plots")
    visualization.plot_all_metrics(results, viz_dir)
    
    print(f"\n✅ Compression complete!")
    print(f"   Results: {results_file}")
    print(f"   Plots: {viz_dir}/")


def main():
    """Main entry point for CLI."""
    parser = argparse.ArgumentParser(
        description='Universal Data Compression Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s myimage.png --algorithm all
  %(prog)s document.pdf --algorithm huffman
  %(prog)s video.mp4 --grayscale
  %(prog)s data.txt --output results/
        """
    )
    
    parser.add_argument('file', help='File to compress')
    parser.add_argument('-a', '--algorithm', 
                       choices=['rle', 'huffman', 'lzw', 'all'],
                       default='all',
                       help='Compression algorithm (default: all)')
    parser.add_argument('-g', '--grayscale',
                       action='store_true',
                       help='Convert images/videos to grayscale')
    parser.add_argument('-o', '--output',
                       default='output',
                       help='Output directory (default: output/)')
    
    args = parser.parse_args()
    
    compress_file(args.file, args.algorithm, args.grayscale, args.output)


if __name__ == '__main__':
    main()
