"""
Image file handler for compression.
Supports PNG, JPG, JPEG, BMP formats.
"""

import numpy as np
from PIL import Image
import io
import os


def load_image(file_path):
    """
    Load image from file.
    
    Args:
        file_path: Path to image file
        
    Returns:
        Tuple of (numpy array, original format, mode)
    """
    img = Image.open(file_path)
    img_array = np.array(img)
    original_format = img.format
    mode = img.mode
    
    return img_array, original_format, mode


def save_image(img_array, file_path, mode='RGB'):
    """
    Save numpy array as image.
    
    Args:
        img_array: Numpy array of image data
        file_path: Path to save image
        mode: Image mode (RGB, L, etc.)
    """
    img = Image.fromarray(img_array.astype('uint8'), mode=mode)
    img.save(file_path)


def image_to_data(img_array):
    """
    Convert image array to flat data list.
    
    Args:
        img_array: Numpy array
        
    Returns:
        Flat list of pixel values
    """
    return img_array.flatten().tolist()


def data_to_image(data, shape, dtype='uint8'):
    """
    Reconstruct image from flat data.
    
    Args:
        data: Flat list of pixel values
        shape: Original image shape
        dtype: Data type
        
    Returns:
        Numpy array
    """
    return np.array(data, dtype=dtype).reshape(shape)


def prepare_for_compression(file_path, grayscale=False, resize=None, resize_percent=None):
    """
    Prepare image for compression.
    
    Args:
        file_path: Path to image
        grayscale: Convert to grayscale
        resize: Tuple (width, height) to resize image, or None to keep original
        resize_percent: Integer percentage (25, 50, 75) to resize by percentage
        
    Returns:
        Dictionary with image data and metadata
    """
    img = Image.open(file_path)
    original_size = img.size
    
    # Resize if requested
    if resize_percent:
        new_width = int(img.size[0] * resize_percent / 100)
        new_height = int(img.size[1] * resize_percent / 100)
        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
    elif resize:
        img = img.resize(resize, Image.Resampling.LANCZOS)
    
    if grayscale:
        img = img.convert('L')
    
    img_array = np.array(img)
    
    # Use delta encoding for better compression
    # Store differences between adjacent pixels instead of absolute values
    flattened = img_array.flatten()
    delta_encoded = [flattened[0]]  # Keep first value as-is
    for i in range(1, len(flattened)):
        delta = int(flattened[i]) - int(flattened[i-1])
        # Wrap around for byte range (-128 to 127 becomes 0 to 255)
        delta_encoded.append((delta + 128) % 256)
    
    return {
        'data': delta_encoded,
        'shape': img_array.shape,
        'mode': img.mode,
        'format': img.format,
        'original_size': os.path.getsize(file_path),
        'resized': resize is not None or resize_percent is not None,
        'original_dimensions': original_size
    }


def reconstruct_image(image_data):
    """
    Reconstruct image from compressed data.
    
    Args:
        image_data: Dictionary with data and metadata
        
    Returns:
        PIL Image object
    """
    data = image_data['data']
    shape = image_data['shape']
    mode = image_data.get('mode', 'RGB')
    
    # Decode delta encoding if needed
    if isinstance(data[0], int) and len(data) > 1:
        # This might be delta encoded, try to decode
        decoded = [data[0]]
        for i in range(1, len(data)):
            # Reverse the delta encoding
            delta = (data[i] - 128) % 256
            value = (decoded[-1] + delta) % 256
            decoded.append(value)
        data = decoded
    
    img_array = np.array(data, dtype='uint8').reshape(shape)
    img = Image.fromarray(img_array, mode=mode)
    
    return img


def decode_delta(delta_encoded):
    """
    Decode delta-encoded data back to original values.
    
    Args:
        delta_encoded: List of delta-encoded values
        
    Returns:
        List of original values
    """
    if not delta_encoded:
        return []
    
    decoded = [delta_encoded[0]]
    for i in range(1, len(delta_encoded)):
        delta = (delta_encoded[i] - 128)
        value = (decoded[-1] + delta) % 256
        decoded.append(value)
    
    return decoded
