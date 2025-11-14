"""
Project Information and Structure
"""

__version__ = "1.0.0"
__author__ = "Data Compression Project"
__description__ = "Universal Data Compression Tool with RLE, Huffman, and LZW algorithms"

PROJECT_STRUCTURE = """
DataCompressionProject/
│
├── algorithms/                 # Core compression algorithms
│   ├── __init__.py
│   ├── rle.py                 # Run Length Encoding
│   ├── huffman.py             # Huffman Coding
│   └── lzw.py                 # Lempel-Ziv-Welch
│
├── handlers/                   # File type handlers
│   ├── __init__.py
│   ├── image_handler.py       # Image processing (PNG, JPG, BMP)
│   ├── video_handler.py       # Video processing (MP4, AVI, MOV)
│   └── document_handler.py    # Document processing (TXT, PDF, DOCX)
│
├── utils/                      # Utility functions
│   ├── __init__.py
│   ├── performance.py         # Performance measurement & comparison
│   └── visualization.py       # Charts and plots
│
├── sample_files/               # Sample test files
│   └── sample_text.txt
│
├── output/                     # Output directory (generated)
│   └── (results and plots saved here)
│
├── compress.py                 # Main CLI application
├── example.py                  # Usage examples
├── Compression_Analysis.ipynb  # Interactive Jupyter notebook
│
├── README.md                   # Full documentation
├── QUICKSTART.md              # Quick start guide
├── requirements.txt           # Python dependencies
└── __init__.py                # This file
"""

SUPPORTED_FORMATS = {
    'images': ['.png', '.jpg', '.jpeg', '.bmp', '.gif'],
    'videos': ['.mp4', '.avi', '.mov', '.mkv'],
    'documents': ['.txt', '.pdf', '.docx', '.csv', '.md']
}

ALGORITHMS = {
    'RLE': {
        'name': 'Run Length Encoding',
        'best_for': 'Repetitive data, simple graphics',
        'complexity': 'O(n)',
        'type': 'Lossless'
    },
    'Huffman': {
        'name': 'Huffman Coding',
        'best_for': 'Text with varying frequencies',
        'complexity': 'O(n log n)',
        'type': 'Lossless'
    },
    'LZW': {
        'name': 'Lempel-Ziv-Welch',
        'best_for': 'Patterns and dictionaries',
        'complexity': 'O(n)',
        'type': 'Lossless'
    }
}

def print_info():
    """Print project information."""
    print(f"Data Compression Project v{__version__}")
    print(f"Author: {__author__}")
    print(f"\n{__description__}")
    print(f"\n{PROJECT_STRUCTURE}")
    print("\nSupported Algorithms:")
    for algo, info in ALGORITHMS.items():
        print(f"  • {algo}: {info['name']}")
        print(f"    Best for: {info['best_for']}")
        print(f"    Complexity: {info['complexity']}")
        print()

if __name__ == '__main__':
    print_info()
