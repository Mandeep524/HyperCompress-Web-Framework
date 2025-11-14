"""
Test Image Compression - Shows detailed output
"""

import sys
import os
from pathlib import Path
import time
import numpy as np
from PIL import Image

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from algorithms import rle, huffman, lzw

def test_image_compression(image_path):
    """Test compression on an image file."""
    print("\n" + "="*70)
    print("IMAGE COMPRESSION TEST")
    print("="*70)
    
    # Load image
    print(f"\n📁 Loading image: {image_path}")
    img = Image.open(image_path)
    print(f"   Format: {img.format}")
    print(f"   Mode: {img.mode}")
    print(f"   Size: {img.size[0]}x{img.size[1]} pixels")
    
    # Convert to grayscale for better compression
    img_gray = img.convert('L')
    img_array = np.array(img_gray)
    data_list = img_array.flatten().tolist()
    
    original_size = len(data_list)
    print(f"   Original data size: {original_size:,} bytes")
    
    results = []
    
    # Test RLE
    print(f"\n{'='*70}")
    print("RLE (Run Length Encoding)")
    print(f"{'='*70}")
    start = time.time()
    compressed_bytes = rle.compress_to_bytes(data_list)
    comp_time = time.time() - start
    
    start = time.time()
    decompressed = rle.decompress_from_bytes(compressed_bytes)
    decomp_time = time.time() - start
    
    compressed_size = len(compressed_bytes)
    ratio = compressed_size / original_size
    saving = ((original_size - compressed_size) / original_size * 100)
    verified = list(decompressed) == data_list
    
    print(f"Original Size:       {original_size:,} bytes")
    print(f"Compressed Size:     {compressed_size:,} bytes")
    print(f"Compression Ratio:   {ratio:.4f}")
    print(f"Space Savings:       {saving:+.2f}%")
    print(f"Compression Time:    {comp_time:.6f}s")
    print(f"Decompression Time:  {decomp_time:.6f}s")
    print(f"Verification:        {'✓ PASSED' if verified else '✗ FAILED'}")
    
    results.append({
        'name': 'RLE',
        'compressed_size': compressed_size,
        'ratio': ratio,
        'saving': saving,
        'comp_time': comp_time,
        'verified': verified
    })
    
    # Test Huffman
    print(f"\n{'='*70}")
    print("Huffman Coding")
    print(f"{'='*70}")
    start = time.time()
    compressed_bytes = huffman.compress_to_bytes(data_list)
    comp_time = time.time() - start
    
    start = time.time()
    decompressed = huffman.decompress_from_bytes(compressed_bytes)
    decomp_time = time.time() - start
    
    compressed_size = len(compressed_bytes)
    ratio = compressed_size / original_size
    saving = ((original_size - compressed_size) / original_size * 100)
    verified = list(decompressed) == data_list
    
    print(f"Original Size:       {original_size:,} bytes")
    print(f"Compressed Size:     {compressed_size:,} bytes")
    print(f"Compression Ratio:   {ratio:.4f}")
    print(f"Space Savings:       {saving:+.2f}%")
    print(f"Compression Time:    {comp_time:.6f}s")
    print(f"Decompression Time:  {decomp_time:.6f}s")
    print(f"Verification:        {'✓ PASSED' if verified else '✗ FAILED'}")
    
    results.append({
        'name': 'Huffman',
        'compressed_size': compressed_size,
        'ratio': ratio,
        'saving': saving,
        'comp_time': comp_time,
        'verified': verified
    })
    
    # Test LZW
    print(f"\n{'='*70}")
    print("LZW (Lempel-Ziv-Welch)")
    print(f"{'='*70}")
    start = time.time()
    compressed_bytes = lzw.compress_to_bytes(data_list)
    comp_time = time.time() - start
    
    start = time.time()
    decompressed = lzw.decompress_from_bytes(compressed_bytes)
    decomp_time = time.time() - start
    
    compressed_size = len(compressed_bytes)
    ratio = compressed_size / original_size
    saving = ((original_size - compressed_size) / original_size * 100)
    verified = list(decompressed) == data_list
    
    print(f"Original Size:       {original_size:,} bytes")
    print(f"Compressed Size:     {compressed_size:,} bytes")
    print(f"Compression Ratio:   {ratio:.4f}")
    print(f"Space Savings:       {saving:+.2f}%")
    print(f"Compression Time:    {comp_time:.6f}s")
    print(f"Decompression Time:  {decomp_time:.6f}s")
    print(f"Verification:        {'✓ PASSED' if verified else '✗ FAILED'}")
    
    results.append({
        'name': 'LZW',
        'compressed_size': compressed_size,
        'ratio': ratio,
        'saving': saving,
        'comp_time': comp_time,
        'verified': verified
    })
    
    # Summary
    print(f"\n{'='*70}")
    print("SUMMARY")
    print(f"{'='*70}")
    
    best_compression = max(results, key=lambda x: x['saving'])
    if best_compression['saving'] > 0:
        print(f"🏆 Best Compression: {best_compression['name']} ({best_compression['saving']:.2f}% saved)")
    else:
        print(f"⚠️  All algorithms expanded the data (no compression achieved)")
        print(f"   Note: Small or complex images may expand due to compression overhead")
    
    fastest = min(results, key=lambda x: x['comp_time'])
    print(f"⚡ Fastest Algorithm: {fastest['name']} ({fastest['comp_time']:.6f}s)")
    
    print("\n" + "="*70 + "\n")

if __name__ == '__main__':
    # Check if image file exists
    test_file = 'test_large.txt'
    if os.path.exists(test_file):
        # Create a simple test image
        print("Creating a test image...")
        img_array = np.random.randint(0, 256, (100, 100), dtype=np.uint8)
        # Add some patterns for better compression
        img_array[0:20, :] = 255  # White strip
        img_array[20:40, :] = 0   # Black strip
        img_array[40:60, :] = 128 # Gray strip
        img_array[60:80, :] = 200 # Light gray strip
        img_array[80:100, :] = 50 # Dark gray strip
        
        img = Image.fromarray(img_array, mode='L')
        test_image = 'test_image.png'
        img.save(test_image)
        print(f"Test image created: {test_image}\n")
        
        test_image_compression(test_image)
    else:
        print("Creating a simple test image for demonstration...")
        # Create a simple grayscale image with patterns
        img_array = np.zeros((100, 100), dtype=np.uint8)
        # Add horizontal stripes
        for i in range(0, 100, 10):
            img_array[i:i+5, :] = 255
            img_array[i+5:i+10, :] = 0
        
        img = Image.fromarray(img_array, mode='L')
        test_image = 'test_pattern_image.png'
        img.save(test_image)
        print(f"Test image created: {test_image}\n")
        
        test_image_compression(test_image)
