"""
Complete Interactive Demo - Data Compression Project
Run this to see all features working!
"""

import sys
import os
import time
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from algorithms import rle, huffman, lzw


def print_header(title):
    """Print a formatted header."""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80 + "\n")


def print_section(title):
    """Print a section header."""
    print("\n" + "-" * 80)
    print(f"  {title}")
    print("-" * 80)


def test_compression(name, compress_func, decompress_func, data, data_str=None, is_huffman=False):
    """Test a compression algorithm."""
    
    # Use appropriate data type for each algorithm
    if is_huffman or name == "LZW":
        test_data = data_str if data_str else ''.join([chr(d) for d in data])
    else:  # RLE
        test_data = data
    
    # Compress
    start = time.time()
    compressed = compress_func(test_data)
    comp_time = time.time() - start
    
    # Get compressed size
    if is_huffman:
        encoded, codes = compressed
        comp_size = len(encoded)
    elif name == "RLE":
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
    
    # Calculate metrics
    orig_size = len(data) if isinstance(data, list) else len(data_str)
    ratio = comp_size / orig_size if orig_size > 0 else 1
    space_saving = ((orig_size - comp_size) / orig_size * 100) if orig_size > 0 else 0
    
    # Verify
    if is_huffman or name == "LZW":
        is_correct = ''.join(decompressed) if is_huffman else decompressed == test_data
        is_correct = is_correct if isinstance(is_correct, bool) else is_correct == test_data
    elif name == "RLE":
        is_correct = list(decompressed) == list(data)
    else:
        is_correct = decompressed == test_data
    
    return {
        'name': name,
        'orig_size': orig_size,
        'comp_size': comp_size,
        'ratio': ratio,
        'saving': space_saving,
        'comp_time': comp_time,
        'decomp_time': decomp_time,
        'correct': is_correct
    }


def print_results(results):
    """Print comparison table."""
    print(f"\n{'Algorithm':<15} {'Original':<12} {'Compressed':<12} {'Ratio':<10} {'Savings':<12} {'Comp Time':<12} {'Decomp Time':<12} {'Status'}")
    print("-" * 105)
    
    for r in results:
        status = "✓ PASS" if r['correct'] else "✗ FAIL"
        savings_str = f"{r['saving']:.2f}%" if r['saving'] >= 0 else f"{abs(r['saving']):.2f}% LARGER"
        
        print(f"{r['name']:<15} {r['orig_size']:<12,} {r['comp_size']:<12,} {r['ratio']:<10.4f} "
              f"{savings_str:<12} {r['comp_time']:<12.6f} {r['decomp_time']:<12.6f} {status}")
    
    print("\n" + "=" * 105)
    
    # Best performers
    valid = [r for r in results if r['saving'] > 0]
    if valid:
        best_ratio = min(valid, key=lambda x: x['ratio'])
        print(f"\n🏆 Best Compression:  {best_ratio['name']} (saved {best_ratio['saving']:.2f}%)")
    
    fastest = min(results, key=lambda x: x['comp_time'])
    print(f"⚡ Fastest Compression: {fastest['name']} ({fastest['comp_time']:.6f}s)")
    
    fastest_d = min(results, key=lambda x: x['decomp_time'])
    print(f"🔄 Fastest Decompression: {fastest_d['name']} ({fastest_d['decomp_time']:.6f}s)")


def demo_text_compression():
    """Demo 1: Text String Compression."""
    print_header("DEMO 1: TEXT STRING COMPRESSION")
    
    # Test 1: Highly repetitive
    print_section("Test 1A: Highly Repetitive Data")
    text1 = "AAAABBBBCCCCDDDD" * 100
    print(f"Text: {text1[:60]}...")
    print(f"Length: {len(text1)} characters")
    
    data1 = [ord(c) for c in text1]
    results1 = []
    results1.append(test_compression("RLE", rle.compress, rle.decompress, data1, text1))
    results1.append(test_compression("Huffman", huffman.compress, huffman.decompress, data1, text1, is_huffman=True))
    results1.append(test_compression("LZW", lzw.compress, lzw.decompress, data1, text1))
    
    print_results(results1)
    print("\n💡 Analysis: RLE excels at repetitive data!")
    
    # Test 2: Natural text
    print_section("Test 1B: Natural Language Text")
    text2 = "The quick brown fox jumps over the lazy dog. " * 200
    print(f"Text: {text2[:60]}...")
    print(f"Length: {len(text2)} characters")
    
    data2 = [ord(c) for c in text2]
    results2 = []
    results2.append(test_compression("RLE", rle.compress, rle.decompress, data2, text2))
    results2.append(test_compression("Huffman", huffman.compress, huffman.decompress, data2, text2, is_huffman=True))
    results2.append(test_compression("LZW", lzw.compress, lzw.decompress, data2, text2))
    
    print_results(results2)
    print("\n💡 Analysis: LZW works best for patterned text!")


def demo_file_compression():
    """Demo 2: File Compression."""
    print_header("DEMO 2: FILE COMPRESSION")
    
    sample_file = "sample_files/sample_text.txt"
    if os.path.exists(sample_file):
        with open(sample_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"File: {sample_file}")
        print(f"Size: {len(content)} characters")
        print(f"Preview:\n{content[:200]}...\n")
        
        data = [ord(c) for c in content]
        results = []
        results.append(test_compression("RLE", rle.compress, rle.decompress, data, content))
        results.append(test_compression("Huffman", huffman.compress, huffman.decompress, data, content, is_huffman=True))
        results.append(test_compression("LZW", lzw.compress, lzw.decompress, data, content))
        
        print_results(results)
        print("\n💡 Analysis: Different algorithms suit different data types!")
    else:
        print(f"⚠️  Sample file not found: {sample_file}")


def demo_algorithm_details():
    """Demo 3: Algorithm Details."""
    print_header("DEMO 3: ALGORITHM DETAILS & EXAMPLES")
    
    # RLE Example
    print_section("Run Length Encoding (RLE)")
    print("Best for: Repetitive data, simple images, binary files")
    print("\nExample:")
    simple_data = [1, 1, 1, 2, 2, 3, 3, 3, 3]
    print(f"  Original: {simple_data}")
    compressed = rle.compress(simple_data)
    print(f"  Compressed: {compressed}")
    decompressed = rle.decompress(compressed)
    print(f"  Decompressed: {decompressed}")
    print(f"  ✓ Match: {decompressed == simple_data}")
    
    # Huffman Example
    print_section("Huffman Coding")
    print("Best for: Text with varying character frequencies")
    print("\nExample:")
    text = "AAABBC"
    print(f"  Original: '{text}'")
    encoded, codes = huffman.compress(text)
    print(f"  Codes: {codes}")
    print(f"  Encoded: {encoded[:50]}..." if len(encoded) > 50 else f"  Encoded: {encoded}")
    decoded = huffman.decompress(encoded, codes)
    print(f"  Decoded: {''.join(decoded)}")
    print(f"  ✓ Match: {''.join(decoded) == text}")
    
    # LZW Example
    print_section("Lempel-Ziv-Welch (LZW)")
    print("Best for: Text with patterns, general-purpose compression")
    print("\nExample:")
    text = "ABABABAB"
    print(f"  Original: '{text}'")
    compressed = lzw.compress(text)
    print(f"  Compressed: {compressed}")
    decompressed = lzw.decompress(compressed)
    print(f"  Decompressed: '{decompressed}'")
    print(f"  ✓ Match: {decompressed == text}")


def demo_comparison_summary():
    """Demo 4: Algorithm Comparison."""
    print_header("DEMO 4: ALGORITHM COMPARISON GUIDE")
    
    print("┌─────────────┬────────────────────────────┬────────────┬───────────────┬──────────────────┐")
    print("│ Algorithm   │ Best For                   │ Speed      │ Compression   │ Use Cases        │")
    print("├─────────────┼────────────────────────────┼────────────┼───────────────┼──────────────────┤")
    print("│ RLE         │ Repetitive data            │ ⚡⚡⚡ Fast  │ Great on reps │ Images, graphics │")
    print("│ Huffman     │ Frequency-based data       │ ⚡⚡ Medium │ Good on text  │ Text, archives   │")
    print("│ LZW         │ Patterns & dictionaries    │ ⚡⚡ Good   │ All-around    │ GIF, general use │")
    print("└─────────────┴────────────────────────────┴────────────┴───────────────┴──────────────────┘")
    
    print("\n📚 Key Insights:")
    print("  • RLE: Simple and fast, but only good for repetitive data")
    print("  • Huffman: Optimal for single-character frequency, used in JPEG/ZIP")
    print("  • LZW: Adaptive dictionary, used in GIF and Unix compress")
    print("\n  • Small files: Compression overhead may exceed savings")
    print("  • Large files: All algorithms perform better")
    print("  • Repetitive data: RLE wins")
    print("  • Natural text: LZW or Huffman work well")


def main():
    """Run all demos."""
    print("\n" + "╔" + "═" * 78 + "╗")
    print("║" + " " * 20 + "DATA COMPRESSION PROJECT - FULL DEMO" + " " * 22 + "║")
    print("║" + " " * 17 + "Comparing RLE, Huffman, and LZW Algorithms" + " " * 19 + "║")
    print("╚" + "═" * 78 + "╝")
    
    try:
        demo_text_compression()
        demo_file_compression()
        demo_algorithm_details()
        demo_comparison_summary()
        
        print_header("✅ ALL DEMOS COMPLETED SUCCESSFULLY!")
        print("\n🚀 Next Steps:")
        print("  1. Open Compression_Analysis.ipynb in Jupyter for interactive visualizations")
        print("  2. Explore the algorithms/ folder to see implementation details")
        print("  3. Try compressing your own files!")
        print("  4. Read README.md for full documentation")
        print("\n📁 Project Location: /Users/mandeepsingh/Downloads/DataCompressionProject/")
        print()
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Demo interrupted by user.")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
