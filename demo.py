"""
Simple compression demo without visualization dependencies.
Demonstrates RLE, Huffman, and LZW compression algorithms.
"""

import sys
import os
import time
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from algorithms import rle, huffman, lzw


def test_algorithm(name, compress_func, decompress_func, data, is_huffman=False, is_rle=False):
    """Test a compression algorithm and measure performance."""
    
    print(f"\n{'='*60}")
    print(f"Testing {name}")
    print(f"{'='*60}")
    
    # Compression
    start = time.time()
    compressed = compress_func(data)
    comp_time = time.time() - start
    
    # Decompression
    start = time.time()
    if is_huffman:
        encoded, codes = compressed
        decompressed = decompress_func(encoded, codes)
        comp_size = len(encoded)
    elif is_rle:
        decompressed = decompress_func(compressed)
        comp_size = len(compressed) * 2  # (value, count) pairs
    else:
        decompressed = decompress_func(compressed)
        comp_size = len(str(compressed))
    decomp_time = time.time() - start
    
    # Calculate metrics
    orig_size = len(data)
    ratio = comp_size / orig_size if orig_size > 0 else 1
    space_saving = ((orig_size - comp_size) / orig_size * 100) if orig_size > 0 else 0
    
    # Verify correctness
    if isinstance(data, str):
        is_correct = (decompressed == data) or (''.join(decompressed) == data)
    else:
        is_correct = (list(decompressed) == list(data))
    
    # Print results
    print(f"Original Size:      {orig_size:,} bytes")
    print(f"Compressed Size:    {comp_size:,} bytes")
    print(f"Compression Ratio:  {ratio:.4f}")
    print(f"Space Savings:      {space_saving:.2f}%")
    print(f"Compression Time:   {comp_time:.6f} seconds")
    print(f"Decompression Time: {decomp_time:.6f} seconds")
    print(f"Verification:       {'✓ PASSED' if is_correct else '✗ FAILED'}")
    
    return {
        'algorithm': name,
        'ratio': ratio,
        'space_saving': space_saving,
        'comp_time': comp_time,
        'decomp_time': decomp_time,
        'correct': is_correct
    }


def main():
    """Run compression demos."""
    
    print("\n" + "="*70)
    print("  DATA COMPRESSION PROJECT - DEMO")
    print("="*70)
    
    # Test 1: Highly Repetitive Text
    print("\n\n📝 TEST 1: Highly Repetitive Text")
    print("-" * 70)
    text1 = "AAAABBBBBCCCCCDDDDDEEEEE" * 50
    print(f"Sample: {text1[:60]}...")
    print(f"Length: {len(text1)} characters")
    
    data1 = [ord(c) for c in text1]
    results1 = []
    
    results1.append(test_algorithm("RLE", rle.compress, rle.decompress, data1, is_rle=True))
    results1.append(test_algorithm("Huffman", 
                                   huffman.compress,
                                   huffman.decompress,
                                   text1, is_huffman=True))
    results1.append(test_algorithm("LZW", lzw.compress, lzw.decompress, text1))
    
    # Test 2: Mixed Content
    print("\n\n📝 TEST 2: Mixed Content Text")
    print("-" * 70)
    text2 = "The quick brown fox jumps over the lazy dog. " * 100
    print(f"Sample: {text2[:60]}...")
    print(f"Length: {len(text2)} characters")
    
    data2 = [ord(c) for c in text2]
    results2 = []
    
    results2.append(test_algorithm("RLE", rle.compress, rle.decompress, data2, is_rle=True))
    results2.append(test_algorithm("Huffman", 
                                   huffman.compress,
                                   huffman.decompress,
                                   text2, is_huffman=True))
    results2.append(test_algorithm("LZW", lzw.compress, lzw.decompress, text2))
    
    # Summary
    print("\n\n" + "="*70)
    print("  SUMMARY - BEST PERFORMERS")
    print("="*70)
    
    all_results = results1 + results2
    
    best_ratio = min(all_results, key=lambda x: x['ratio'])
    print(f"\n🏆 Best Compression Ratio: {best_ratio['algorithm']} ({best_ratio['ratio']:.4f})")
    
    best_speed = min(all_results, key=lambda x: x['comp_time'])
    print(f"⚡ Fastest Compression:    {best_speed['algorithm']} ({best_speed['comp_time']:.6f}s)")
    
    best_decomp = min(all_results, key=lambda x: x['decomp_time'])
    print(f"🔄 Fastest Decompression:  {best_decomp['algorithm']} ({best_decomp['decomp_time']:.6f}s)")
    
    # Load sample file if it exists
    sample_file = "sample_files/sample_text.txt"
    if os.path.exists(sample_file):
        print("\n\n📄 TEST 3: Sample File")
        print("-" * 70)
        with open(sample_file, 'r', encoding='utf-8') as f:
            file_content = f.read()
        
        print(f"File: {sample_file}")
        print(f"Size: {len(file_content)} characters")
        print(f"Preview: {file_content[:100]}...")
        
        data3 = [ord(c) for c in file_content]
        
        test_algorithm("RLE", rle.compress, rle.decompress, data3, is_rle=True)
        test_algorithm("Huffman", 
                      huffman.compress,
                      huffman.decompress,
                      file_content, is_huffman=True)
        test_algorithm("LZW", lzw.compress, lzw.decompress, file_content)
    
    print("\n\n" + "="*70)
    print("  ✅ DEMO COMPLETE!")
    print("="*70)
    print("\nNext steps:")
    print("  1. Open Compression_Analysis.ipynb for interactive demos")
    print("  2. Try: python compress.py yourfile.txt (requires matplotlib)")
    print("  3. Explore the algorithms/ folder for implementation details")
    print("\n")


if __name__ == '__main__':
    main()
