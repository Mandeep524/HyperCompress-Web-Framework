"""
Video file handler for compression.
Supports MP4, AVI, MOV formats.
"""

import cv2
import numpy as np
import os


def load_video(file_path, max_frames=None):
    """
    Load video from file.
    
    Args:
        file_path: Path to video file
        max_frames: Maximum number of frames to load (None for all)
        
    Returns:
        Dictionary with frames and metadata
    """
    cap = cv2.VideoCapture(file_path)
    
    if not cap.isOpened():
        raise ValueError(f"Could not open video file: {file_path}")
    
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    frames = []
    frame_count = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        frames.append(frame)
        frame_count += 1
        
        if max_frames and frame_count >= max_frames:
            break
    
    cap.release()
    
    return {
        'frames': frames,
        'fps': fps,
        'width': width,
        'height': height,
        'total_frames': total_frames,
        'loaded_frames': frame_count,
        'original_size': os.path.getsize(file_path)
    }


def save_video(frames, output_path, fps=30, codec='mp4v'):
    """
    Save frames as video.
    
    Args:
        frames: List of frame arrays
        output_path: Path to save video
        fps: Frames per second
        codec: Video codec (mp4v, XVID, etc.)
    """
    if not frames:
        raise ValueError("No frames to save")
    
    height, width = frames[0].shape[:2]
    fourcc = cv2.VideoWriter_fourcc(*codec)
    
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    for frame in frames:
        out.write(frame)
    
    out.release()


def prepare_for_compression(file_path, grayscale=False, max_frames=100):
    """
    Prepare video for compression by extracting frames.
    
    Args:
        file_path: Path to video
        grayscale: Convert to grayscale
        max_frames: Maximum frames to process
        
    Returns:
        Dictionary with video data and metadata
    """
    cap = cv2.VideoCapture(file_path)
    
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    frames_data = []
    frame_count = 0
    
    while frame_count < max_frames:
        ret, frame = cap.read()
        if not ret:
            break
        
        if grayscale:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        frames_data.append(frame.flatten().tolist())
        frame_count += 1
    
    cap.release()
    
    return {
        'data': frames_data,
        'fps': fps,
        'width': width,
        'height': height,
        'frame_count': frame_count,
        'grayscale': grayscale,
        'original_size': os.path.getsize(file_path)
    }


def reconstruct_video(video_data):
    """
    Reconstruct video frames from compressed data.
    
    Args:
        video_data: Dictionary with data and metadata
        
    Returns:
        List of frame arrays
    """
    frames = []
    width = video_data['width']
    height = video_data['height']
    grayscale = video_data.get('grayscale', False)
    
    for frame_data in video_data['data']:
        if grayscale:
            shape = (height, width)
        else:
            shape = (height, width, 3)
        
        frame = np.array(frame_data, dtype='uint8').reshape(shape)
        frames.append(frame)
    
    return frames
