"""
Run Length Encoding (RLE) Compression Algorithm
Best for data with long runs of repeated values (e.g., binary images, simple graphics)
"""

import pickle


def compress(data):
    """
    Compress data using Run Length Encoding.
    
    Args:
        data: List or bytes to compress
        
    Returns:
        List of tuples (value, count)
    """
    if not data:
        return []
    
    compressed = []
    prev = data[0]
    count = 1
    
    for i in range(1, len(data)):
        if data[i] == prev:
            count += 1
        else:
            compressed.append((prev, count))
            prev = data[i]
            count = 1
    
    compressed.append((prev, count))
    return compressed


def decompress(compressed_data):
    """
    Decompress RLE compressed data.
    
    Args:
        compressed_data: List of tuples (value, count)
        
    Returns:
        Original data as list
    """
    if not compressed_data:
        return []
    
    decompressed = []
    for value, count in compressed_data:
        decompressed.extend([value] * count)
    
    return decompressed


def compress_to_bytes(data):
    """
    Compress data and convert to bytes for storage.
    
    Args:
        data: Input data (list or bytes)
        
    Returns:
        Compressed data as bytes
    """
    compressed = compress(data)
    return pickle.dumps(compressed, protocol=pickle.HIGHEST_PROTOCOL)


def decompress_from_bytes(compressed_bytes):
    """
    Decompress data from bytes.
    
    Args:
        compressed_bytes: Compressed data as bytes
        
    Returns:
        Original data as list
    """
    compressed_data = pickle.loads(compressed_bytes)
    return decompress(compressed_data)


def compress_string(text):
    """
    Compress a string using RLE (alternative string-based format).
    
    Args:
        text: String to compress
        
    Returns:
        Compressed string with format: count+character
    """
    if not text:
        return ""
    
    compressed = ""
    i = 0
    
    while i < len(text):
        count = 1
        while i + 1 < len(text) and text[i] == text[i + 1]:
            count += 1
            i += 1
        compressed += str(count) + text[i]
        i += 1
    
    return compressed


def decompress_string(compressed_text):
    """
    Decompress RLE string format.
    
    Args:
        compressed_text: Compressed string
        
    Returns:
        Original string
    """
    if not compressed_text:
        return ""
    
    decompressed = ""
    count = ""
    
    for char in compressed_text:
        if char.isdigit():
            count += char
        else:
            decompressed += char * int(count)
            count = ""
    
    return decompressed
