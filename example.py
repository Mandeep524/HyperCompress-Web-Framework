# Example usage of the compression library

from algorithms import rle, huffman, lzw

# Example 1: Compress a simple string
text = "AAAABBBBBCCCCC"
print(f"Original: {text}")

# RLE
rle_compressed = rle.compress_string(text)
print(f"RLE: {rle_compressed}")
print(f"RLE Decompressed: {rle.decompress_string(rle_compressed)}")

# Huffman
huffman_encoded, huffman_codes = huffman.compress(text)
print(f"Huffman: {huffman_encoded[:50]}... (bitstring)")
print(f"Huffman Codes: {huffman_codes}")

# LZW
lzw_compressed = lzw.compress(text)
print(f"LZW: {lzw_compressed}")
print(f"LZW Decompressed: {lzw.decompress(lzw_compressed)}")

# Example 2: Performance comparison
from utils import performance

data = [ord(c) for c in text]
algorithms = [
    ('RLE', rle.compress, rle.decompress, False),
    ('Huffman', lambda d: huffman.compress(text), lambda c: huffman.decompress(c[0], c[1]), True),
    ('LZW', lambda d: lzw.compress(text), lzw.decompress, False)
]

results = performance.compare_algorithms(data, algorithms)
performance.print_comparison_table(results)
