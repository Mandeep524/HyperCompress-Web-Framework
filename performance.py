"""
Utility functions for compression analysis and performance measurement.
"""

import time
import os
import json
from typing import Callable, Any, Dict


def measure_compression(compress_func: Callable, decompress_func: Callable, 
                       data: Any, algorithm_name: str, 
                       is_huffman: bool = False) -> Dict:
    """
    Measure compression performance.
    
    Args:
        compress_func: Compression function
        decompress_func: Decompression function
        data: Data to compress
        algorithm_name: Name of algorithm
        is_huffman: Whether using Huffman coding
        
    Returns:
        Dictionary with performance metrics
    """
    # Compression timing
    start_time = time.time()
    compressed = compress_func(data)
    compression_time = time.time() - start_time
    
    # Decompression timing
    start_time = time.time()
    if is_huffman:
        encoded, codes = compressed
        decompressed = decompress_func(encoded, codes)
        compressed_size = len(encoded)
    else:
        decompressed = decompress_func(compressed)
        compressed_size = len(str(compressed))
    
    decompression_time = time.time() - start_time
    
    # Calculate metrics
    original_size = len(str(data))
    compression_ratio = compressed_size / original_size if original_size > 0 else 1
    space_saving = ((original_size - compressed_size) / original_size * 100) if original_size > 0 else 0
    
    # Verify correctness
    if isinstance(data, str):
        is_correct = decompressed == data or ''.join(decompressed) == data
    elif isinstance(data, list):
        is_correct = list(decompressed) == data
    else:
        is_correct = decompressed == data
    
    return {
        'algorithm': algorithm_name,
        'original_size': original_size,
        'compressed_size': compressed_size,
        'compression_ratio': round(compression_ratio, 4),
        'space_saving_percent': round(space_saving, 2),
        'compression_time': round(compression_time, 6),
        'decompression_time': round(decompression_time, 6),
        'total_time': round(compression_time + decompression_time, 6),
        'is_correct': is_correct
    }


def compare_algorithms(data: Any, algorithms: list) -> list:
    """
    Compare multiple compression algorithms.
    
    Args:
        data: Data to compress
        algorithms: List of tuples (name, compress_func, decompress_func, is_huffman)
        
    Returns:
        List of performance dictionaries
    """
    results = []
    
    for name, compress_func, decompress_func, is_huffman in algorithms:
        try:
            result = measure_compression(
                compress_func, decompress_func, data, name, is_huffman
            )
            results.append(result)
        except Exception as e:
            print(f"Error with {name}: {str(e)}")
            results.append({
                'algorithm': name,
                'error': str(e)
            })
    
    return results


def format_size(size_bytes: int) -> str:
    """
    Format byte size to human-readable string.
    
    Args:
        size_bytes: Size in bytes
        
    Returns:
        Formatted string (e.g., "1.5 MB")
    """
    size = float(size_bytes)
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return f"{size:.2f} {unit}"
        size /= 1024.0
    return f"{size:.2f} PB"


def save_results(results: list, output_path: str):
    """
    Save compression results to JSON file.
    
    Args:
        results: List of result dictionaries
        output_path: Path to save results
    """
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"Results saved to: {output_path}")


def load_results(input_path: str) -> list:
    """
    Load compression results from JSON file.
    
    Args:
        input_path: Path to results file
        
    Returns:
        List of result dictionaries
    """
    with open(input_path, 'r') as f:
        return json.load(f)


def print_comparison_table(results: list):
    """
    Print a formatted comparison table of results.
    
    Args:
        results: List of result dictionaries
    """
    if not results:
        print("No results to display")
        return
    
    # Header
    print("\n" + "="*100)
    print(f"{'Algorithm':<15} {'Orig Size':<12} {'Comp Size':<12} {'Ratio':<10} "
          f"{'Saving %':<10} {'Comp Time':<12} {'Decomp Time':<12}")
    print("="*100)
    
    # Results
    for result in results:
        if 'error' in result:
            print(f"{result['algorithm']:<15} ERROR: {result['error']}")
        else:
            print(f"{result['algorithm']:<15} "
                  f"{result['original_size']:<12} "
                  f"{result['compressed_size']:<12} "
                  f"{result['compression_ratio']:<10.4f} "
                  f"{result['space_saving_percent']:<10.2f} "
                  f"{result['compression_time']:<12.6f} "
                  f"{result['decompression_time']:<12.6f}")
    
    print("="*100)
    
    # Best performers
    valid_results = [r for r in results if 'error' not in r]
    
    if valid_results:
        print("\n📊 Best Performers:")
        
        best_ratio = min(valid_results, key=lambda x: x['compression_ratio'])
        print(f"   🏆 Best Compression Ratio: {best_ratio['algorithm']} ({best_ratio['compression_ratio']:.4f})")
        
        best_speed = min(valid_results, key=lambda x: x['compression_time'])
        print(f"   ⚡ Fastest Compression: {best_speed['algorithm']} ({best_speed['compression_time']:.6f}s)")
        
        best_decomp = min(valid_results, key=lambda x: x['decompression_time'])
        print(f"   🔄 Fastest Decompression: {best_decomp['algorithm']} ({best_decomp['decompression_time']:.6f}s)")
        
        print()
