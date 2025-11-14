"""
Huffman Coding Compression Algorithm
Best for text and data with varying character frequencies
Uses variable-length codes based on frequency analysis
"""

from collections import defaultdict
from heapq import heappush, heappop, heapify
import pickle


class HuffmanNode:
    """Node for building Huffman tree."""
    
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left: 'HuffmanNode | None' = None
        self.right: 'HuffmanNode | None' = None
    
    def __lt__(self, other):
        return self.freq < other.freq


def build_frequency_table(data):
    """Build frequency table from data."""
    freq = defaultdict(int)
    for item in data:
        freq[item] += 1
    return freq


def build_huffman_tree(data):
    """
    Build Huffman tree from data.
    
    Args:
        data: Input data (string, bytes, or list)
        
    Returns:
        Root node of Huffman tree
    """
    freq = build_frequency_table(data)
    
    if len(freq) == 0:
        return None
    
    if len(freq) == 1:
        # Special case: only one unique character
        char = list(freq.keys())[0]
        root = HuffmanNode(char, freq[char])
        return root
    
    heap = [HuffmanNode(ch, fr) for ch, fr in freq.items()]
    heapify(heap)
    
    while len(heap) > 1:
        node1 = heappop(heap)
        node2 = heappop(heap)
        
        merged = HuffmanNode(None, node1.freq + node2.freq)
        merged.left = node1
        merged.right = node2
        
        heappush(heap, merged)
    
    return heap[0]


def build_codes(node, prefix="", code_map=None):
    """
    Build Huffman codes from tree.
    
    Args:
        node: Root of Huffman tree
        prefix: Current code prefix
        code_map: Dictionary to store codes
        
    Returns:
        Dictionary mapping characters to codes
    """
    if code_map is None:
        code_map = {}
    
    if node is None:
        return code_map
    
    if node.char is not None:
        code_map[node.char] = prefix if prefix else "0"
    
    build_codes(node.left, prefix + "0", code_map)
    build_codes(node.right, prefix + "1", code_map)
    
    return code_map


def compress(data):
    """
    Compress data using Huffman coding.
    
    Args:
        data: Input data (string, bytes, or list)
        
    Returns:
        Tuple of (encoded bitstring, code dictionary)
    """
    if not data:
        return ("", {})
    
    root = build_huffman_tree(data)
    codes = build_codes(root)
    
    encoded = ''.join([codes[item] for item in data])
    
    return (encoded, codes)


def decompress(encoded_data, codes):
    """
    Decompress Huffman encoded data.
    
    Args:
        encoded_data: Encoded bitstring
        codes: Code dictionary from compression
        
    Returns:
        Original data
    """
    if not encoded_data:
        return ""
    
    reverse_codes = {v: k for k, v in codes.items()}
    
    decoded = []
    buffer = ""
    
    for bit in encoded_data:
        buffer += bit
        if buffer in reverse_codes:
            decoded.append(reverse_codes[buffer])
            buffer = ""
    
    return decoded


def compress_to_bytes(data):
    """
    Compress data and convert to bytes for storage.
    Optimized to store frequency table instead of full codebook.
    
    Args:
        data: Input data
        
    Returns:
        Compressed data as bytes
    """
    if not data:
        return b''
    
    encoded, codes = compress(data)
    
    # Convert bitstring to bytes
    padding = 8 - len(encoded) % 8
    if padding != 8:
        encoded += '0' * padding
    
    byte_array = bytearray()
    for i in range(0, len(encoded), 8):
        byte = encoded[i:i+8]
        byte_array.append(int(byte, 2))
    
    # Store only frequency table (much smaller than full codebook)
    freq_table = build_frequency_table(data)
    
    # Store padding info, frequency table, and compressed data
    result = {
        'padding': padding,
        'freq': dict(freq_table),  # Convert to regular dict for pickle
        'data': bytes(byte_array)
    }
    
    return pickle.dumps(result, protocol=pickle.HIGHEST_PROTOCOL)


def decompress_from_bytes(compressed_bytes):
    """
    Decompress data from bytes.
    Rebuilds Huffman tree from frequency table.
    
    Args:
        compressed_bytes: Compressed data as bytes
        
    Returns:
        Original data
    """
    if not compressed_bytes:
        return []
    
    result = pickle.loads(compressed_bytes)
    
    padding = result['padding']
    freq_table = result['freq']
    byte_data = result['data']
    
    # Rebuild Huffman tree from frequency table
    heap = [HuffmanNode(ch, fr) for ch, fr in freq_table.items()]
    
    if len(heap) == 1:
        # Special case: only one unique character
        node = heap[0]
        codes = {node.char: "0"}
    else:
        heapify(heap)
        while len(heap) > 1:
            node1 = heappop(heap)
            node2 = heappop(heap)
            merged = HuffmanNode(None, node1.freq + node2.freq)
            merged.left = node1
            merged.right = node2
            heappush(heap, merged)
        codes = build_codes(heap[0])
    
    # Convert bytes back to bitstring
    bitstring = ''.join([bin(byte)[2:].zfill(8) for byte in byte_data])
    
    # Remove padding
    if padding != 8:
        bitstring = bitstring[:-padding]
    
    return decompress(bitstring, codes)
