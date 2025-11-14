"""
Demonstration of Lossy vs Lossless vs RLE Compression on Images
"""
import numpy as np
from PIL import Image
import os
from algorithms import rle, huffman, lzw

def create_sample_images():
    """Create sample images for testing different compression types."""
    
    # 1. Create a simple striped pattern (ideal for RLE)
    print("Creating sample images...")
    width, height = 400, 400
    
    # Striped image - perfect for RLE
    striped = np.zeros((height, width), dtype=np.uint8)
    for i in range(0, height, 20):
        striped[i:i+10, :] = 255
    striped_img = Image.fromarray(striped, mode='L')
    striped_img.save('sample_striped.png')
    
    # Gradient image - better for Huffman/LZW
    gradient = np.zeros((height, width), dtype=np.uint8)
    for i in range(height):
        gradient[i, :] = int((i / height) * 255)
    gradient_img = Image.fromarray(gradient, mode='L')
    gradient_img.save('sample_gradient.png')
    
    print("✓ Created: sample_striped.png (for RLE)")
    print("✓ Created: sample_gradient.png (for Huffman/LZW)")
    print()
    
    return 'sample_striped.png', 'sample_gradient.png'

def demonstrate_rle_compression(image_path):
    """Demonstrate RLE (Run Length Encoding) - Lossless."""
    print("=" * 60)
    print("RLE (Run Length Encoding) - LOSSLESS Compression")
    print("=" * 60)
    
    img = Image.open(image_path).convert('L')
    img_array = np.array(img)
    data_list = img_array.flatten().tolist()
    
    print(f"Image: {image_path}")
    print(f"Size: {img.size[0]}x{img.size[1]} pixels")
    print(f"Original data size: {len(data_list)} bytes")
    
    # Compress with RLE
    compressed = rle.compress(data_list)
    compressed_bytes = rle.compress_to_bytes(data_list)
    
    print(f"Compressed size: {len(compressed_bytes)} bytes")
    print(f"Compression ratio: {len(compressed_bytes)/len(data_list):.4f}")
    print(f"Space saved: {(1 - len(compressed_bytes)/len(data_list)) * 100:.2f}%")
    
    # Decompress and verify
    decompressed = rle.decompress_from_bytes(compressed_bytes)
    verified = list(decompressed) == data_list
    print(f"Lossless verification: {'✓ PASSED' if verified else '✗ FAILED'}")
    
    # Save decompressed image
    decompressed_array = np.array(list(decompressed), dtype=np.uint8).reshape(img_array.shape)
    decompressed_img = Image.fromarray(decompressed_array, mode='L')
    output_name = image_path.replace('.png', '_rle_decompressed.png')
    decompressed_img.save(output_name)
    print(f"Saved: {output_name}")
    print()

def demonstrate_lossless_compression(image_path):
    """Demonstrate Huffman and LZW - Lossless Compression."""
    print("=" * 60)
    print("Huffman & LZW - LOSSLESS Compression")
    print("=" * 60)
    
    img = Image.open(image_path).convert('L')
    img_array = np.array(img)
    data_list = img_array.flatten().tolist()
    
    print(f"Image: {image_path}")
    print(f"Size: {img.size[0]}x{img.size[1]} pixels")
    print(f"Original data size: {len(data_list)} bytes")
    print()
    
    # Huffman Compression
    print("--- Huffman Coding ---")
    compressed_huffman = huffman.compress_to_bytes(data_list)
    print(f"Compressed size: {len(compressed_huffman)} bytes")
    print(f"Compression ratio: {len(compressed_huffman)/len(data_list):.4f}")
    print(f"Space saved: {(1 - len(compressed_huffman)/len(data_list)) * 100:.2f}%")
    
    decompressed_huffman = huffman.decompress_from_bytes(compressed_huffman)
    verified_huffman = list(decompressed_huffman) == data_list
    print(f"Lossless verification: {'✓ PASSED' if verified_huffman else '✗ FAILED'}")
    
    # Save Huffman decompressed
    decompressed_array = np.array(list(decompressed_huffman), dtype=np.uint8).reshape(img_array.shape)
    decompressed_img = Image.fromarray(decompressed_array, mode='L')
    output_name = image_path.replace('.png', '_huffman_decompressed.png')
    decompressed_img.save(output_name)
    print(f"Saved: {output_name}")
    print()
    
    # LZW Compression
    print("--- LZW (Lempel-Ziv-Welch) ---")
    compressed_lzw = lzw.compress_to_bytes(data_list)
    print(f"Compressed size: {len(compressed_lzw)} bytes")
    print(f"Compression ratio: {len(compressed_lzw)/len(data_list):.4f}")
    print(f"Space saved: {(1 - len(compressed_lzw)/len(data_list)) * 100:.2f}%")
    
    decompressed_lzw = lzw.decompress_from_bytes(compressed_lzw)
    verified_lzw = list(decompressed_lzw) == data_list
    print(f"Lossless verification: {'✓ PASSED' if verified_lzw else '✗ FAILED'}")
    
    # Save LZW decompressed
    decompressed_array = np.array(list(decompressed_lzw), dtype=np.uint8).reshape(img_array.shape)
    decompressed_img = Image.fromarray(decompressed_array, mode='L')
    output_name = image_path.replace('.png', '_lzw_decompressed.png')
    decompressed_img.save(output_name)
    print(f"Saved: {output_name}")
    print()

def demonstrate_lossy_compression(image_path):
    """Demonstrate Lossy Compression using JPEG."""
    print("=" * 60)
    print("JPEG - LOSSY Compression")
    print("=" * 60)
    
    img = Image.open(image_path).convert('L')
    
    print(f"Image: {image_path}")
    print(f"Size: {img.size[0]}x{img.size[1]} pixels")
    
    # Get original file size
    original_size = os.path.getsize(image_path)
    print(f"Original PNG file size: {original_size} bytes")
    print()
    
    # Save with different JPEG quality levels
    qualities = [95, 75, 50, 25, 10]
    
    for quality in qualities:
        output_name = image_path.replace('.png', f'_jpeg_q{quality}.jpg')
        img.save(output_name, 'JPEG', quality=quality)
        
        compressed_size = os.path.getsize(output_name)
        ratio = compressed_size / original_size
        saved = (1 - ratio) * 100
        
        print(f"Quality {quality}%:")
        print(f"  File size: {compressed_size} bytes")
        print(f"  Compression ratio: {ratio:.4f}")
        print(f"  Space saved: {saved:.2f}%")
        print(f"  Saved: {output_name}")
        
        # Reload and check difference
        lossy_img = Image.open(output_name).convert('L')
        original_array = np.array(img)
        lossy_array = np.array(lossy_img)
        
        # Calculate difference
        diff = np.abs(original_array.astype(int) - lossy_array.astype(int))
        max_diff = np.max(diff)
        avg_diff = np.mean(diff)
        
        print(f"  Max pixel difference: {max_diff}")
        print(f"  Avg pixel difference: {avg_diff:.2f}")
        print(f"  Lossless: {'✗ NO (lossy)' if max_diff > 0 else '✓ YES'}")
        print()

def main():
    print()
    print("╔" + "=" * 58 + "╗")
    print("║  IMAGE COMPRESSION COMPARISON DEMO                       ║")
    print("║  Lossy vs Lossless vs RLE                                ║")
    print("╚" + "=" * 58 + "╝")
    print()
    
    # Create sample images
    striped_path, gradient_path = create_sample_images()
    
    # Demonstrate RLE on striped pattern (best case for RLE)
    demonstrate_rle_compression(striped_path)
    
    # Demonstrate lossless compression on gradient
    demonstrate_lossless_compression(gradient_path)
    
    # Demonstrate lossy compression
    demonstrate_lossy_compression(gradient_path)
    
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print("✓ LOSSLESS Compression (RLE, Huffman, LZW):")
    print("  - Decompressed data exactly matches original")
    print("  - No quality loss")
    print("  - Good for text, medical images, legal documents")
    print()
    print("✗ LOSSY Compression (JPEG):")
    print("  - Some data is permanently lost")
    print("  - Better compression ratios")
    print("  - Good for photos where small quality loss is acceptable")
    print()
    print("📊 All output files have been saved to current directory")
    print("=" * 60)

if __name__ == "__main__":
    main()
