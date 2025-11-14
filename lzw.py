"""
Lempel-Ziv-Welch (LZW) Compression Algorithm
Best for text and data with repeating patterns
Dictionary-based compression that builds patterns dynamically
"""

import pickle


def compress(data):
    """
    Compress data using LZW algorithm.
    
    Args:
        data: String or bytes to compress
        
    Returns:
        List of integers representing compressed data
    """
    if not data:
        return []
    
    # Initialize dictionary with single characters
    dict_size = 256
    dictionary = {chr(i): i for i in range(dict_size)}
    
    w = ""
    result = []
    
    for c in data:
        wc = w + c
        if wc in dictionary:
            w = wc
        else:
            result.append(dictionary[w])
            dictionary[wc] = dict_size
            dict_size += 1
            w = c
    
    if w:
        result.append(dictionary[w])
    
    return result


def decompress(compressed_data):
    """
    Decompress LZW compressed data.
    
    Args:
        compressed_data: List of integers from compression
        
    Returns:
        Original string
    """
    if not compressed_data:
        return ""
    
    # Initialize dictionary
    dict_size = 256
    dictionary = {i: chr(i) for i in range(dict_size)}
    
    # Make a copy to avoid modifying the input
    compressed = list(compressed_data)
    
    w = chr(compressed.pop(0))
    result = w
    
    for k in compressed:
        if k in dictionary:
            entry = dictionary[k]
        elif k == dict_size:
            entry = w + w[0]
        else:
            raise ValueError(f"Bad compressed key: {k}")
        
        result += entry
        dictionary[dict_size] = w + entry[0]
        dict_size += 1
        w = entry
    
    return result


def compress_to_bytes(data):
    """
    Compress data and convert to bytes for storage.
    
    Args:
        data: Input data (list of integers or string)
        
    Returns:
        Compressed data as bytes
    """
    # Convert list of integers to string if needed
    if isinstance(data, list):
        # Ensure all values are valid bytes (0-255)
        try:
            text = ''.join([chr(x % 256) for x in data])
        except Exception as e:
            # Fallback: convert to string representation
            text = str(data)
    else:
        text = str(data) if not isinstance(data, str) else data
    
    compressed = compress(text)
    return pickle.dumps(compressed, protocol=pickle.HIGHEST_PROTOCOL)


def decompress_from_bytes(compressed_bytes):
    """
    Decompress data from bytes.
    
    Args:
        compressed_bytes: Compressed data as bytes
        
    Returns:
        Original data as list of integers
    """
    compressed_data = pickle.loads(compressed_bytes)
    text = decompress(compressed_data)
    return [ord(c) for c in text]


def compress_bytes(data):
    """
    Compress bytes data using LZW.
    
    Args:
        data: Bytes to compress
        
    Returns:
        List of integers
    """
    # Convert bytes to string for LZW processing
    text = ''.join([chr(b) for b in data])
    return compress(text)


def decompress_to_bytes(compressed_data):
    """
    Decompress LZW data back to bytes.
    
    Args:
        compressed_data: List of integers
        
    Returns:
        Original bytes
    """
    text = decompress(compressed_data)
    return bytes([ord(c) for c in text])
