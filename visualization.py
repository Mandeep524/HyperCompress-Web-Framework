"""
Visualization utilities for compression analysis.
"""

import matplotlib.pyplot as plt
import pandas as pd
import os


def plot_compression_ratios(results: list, save_path: str = None):
    """
    Plot compression ratios comparison.
    
    Args:
        results: List of result dictionaries
        save_path: Optional path to save figure
    """
    valid_results = [r for r in results if 'error' not in r]
    
    if not valid_results:
        print("No valid results to plot")
        return
    
    algorithms = [r['algorithm'] for r in valid_results]
    ratios = [r['compression_ratio'] for r in valid_results]
    
    plt.figure(figsize=(10, 6))
    bars = plt.bar(algorithms, ratios, color='steelblue', alpha=0.7)
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.4f}',
                ha='center', va='bottom', fontsize=10)
    
    plt.xlabel('Algorithm', fontsize=12)
    plt.ylabel('Compression Ratio (lower is better)', fontsize=12)
    plt.title('Compression Ratio Comparison', fontsize=14, fontweight='bold')
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Saved: {save_path}")
    
    plt.show()


def plot_compression_times(results: list, save_path: str = None):
    """
    Plot compression times comparison.
    
    Args:
        results: List of result dictionaries
        save_path: Optional path to save figure
    """
    valid_results = [r for r in results if 'error' not in r]
    
    if not valid_results:
        print("No valid results to plot")
        return
    
    algorithms = [r['algorithm'] for r in valid_results]
    comp_times = [r['compression_time'] for r in valid_results]
    
    plt.figure(figsize=(10, 6))
    bars = plt.bar(algorithms, comp_times, color='coral', alpha=0.7)
    
    # Add value labels
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.6f}s',
                ha='center', va='bottom', fontsize=10)
    
    plt.xlabel('Algorithm', fontsize=12)
    plt.ylabel('Compression Time (seconds)', fontsize=12)
    plt.title('Compression Time Comparison', fontsize=14, fontweight='bold')
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Saved: {save_path}")
    
    plt.show()


def plot_decompression_times(results: list, save_path: str = None):
    """
    Plot decompression times comparison.
    
    Args:
        results: List of result dictionaries
        save_path: Optional path to save figure
    """
    valid_results = [r for r in results if 'error' not in r]
    
    if not valid_results:
        print("No valid results to plot")
        return
    
    algorithms = [r['algorithm'] for r in valid_results]
    decomp_times = [r['decompression_time'] for r in valid_results]
    
    plt.figure(figsize=(10, 6))
    bars = plt.bar(algorithms, decomp_times, color='mediumseagreen', alpha=0.7)
    
    # Add value labels
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.6f}s',
                ha='center', va='bottom', fontsize=10)
    
    plt.xlabel('Algorithm', fontsize=12)
    plt.ylabel('Decompression Time (seconds)', fontsize=12)
    plt.title('Decompression Time Comparison', fontsize=14, fontweight='bold')
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Saved: {save_path}")
    
    plt.show()


def plot_space_savings(results: list, save_path: str = None):
    """
    Plot space savings percentage comparison.
    
    Args:
        results: List of result dictionaries
        save_path: Optional path to save figure
    """
    valid_results = [r for r in results if 'error' not in r]
    
    if not valid_results:
        print("No valid results to plot")
        return
    
    algorithms = [r['algorithm'] for r in valid_results]
    savings = [r['space_saving_percent'] for r in valid_results]
    
    plt.figure(figsize=(10, 6))
    bars = plt.bar(algorithms, savings, color='purple', alpha=0.7)
    
    # Add value labels
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.2f}%',
                ha='center', va='bottom', fontsize=10)
    
    plt.xlabel('Algorithm', fontsize=12)
    plt.ylabel('Space Savings (%)', fontsize=12)
    plt.title('Space Savings Comparison', fontsize=14, fontweight='bold')
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Saved: {save_path}")
    
    plt.show()


def plot_all_metrics(results: list, output_dir: str = None):
    """
    Create all visualization plots.
    
    Args:
        results: List of result dictionaries
        output_dir: Directory to save plots
    """
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
    
    # Compression ratio
    save_path = os.path.join(output_dir, 'compression_ratio.png') if output_dir else None
    plot_compression_ratios(results, save_path)
    
    # Compression time
    save_path = os.path.join(output_dir, 'compression_time.png') if output_dir else None
    plot_compression_times(results, save_path)
    
    # Decompression time
    save_path = os.path.join(output_dir, 'decompression_time.png') if output_dir else None
    plot_decompression_times(results, save_path)
    
    # Space savings
    save_path = os.path.join(output_dir, 'space_savings.png') if output_dir else None
    plot_space_savings(results, save_path)


def create_comparison_dataframe(results: list) -> pd.DataFrame:
    """
    Create a pandas DataFrame from results.
    
    Args:
        results: List of result dictionaries
        
    Returns:
        pandas DataFrame
    """
    valid_results = [r for r in results if 'error' not in r]
    df = pd.DataFrame(valid_results)
    
    # Select and order columns
    columns = ['algorithm', 'original_size', 'compressed_size', 'compression_ratio', 
               'space_saving_percent', 'compression_time', 'decompression_time', 
               'total_time', 'is_correct']
    
    df = df[columns]
    
    return df
