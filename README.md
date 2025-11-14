# 📦 Universal Data Compression Project

A comprehensive Python project for comparing different compression algorithms across various data types including images, videos, documents, and text files.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 🎯 Features

- **Multiple Compression Algorithms:**
  - **RLE (Run Length Encoding)** - Best for repetitive data
  - **Huffman Coding** - Optimal for text with varying frequencies
  - **LZW (Lempel-Ziv-Welch)** - Dictionary-based compression

- **Support for Various Data Types:**
  - 📝 Text files (.txt, .csv, .md)
  - 📄 Documents (.pdf, .docx)
  - 🖼️ Images (.png, .jpg, .bmp)
  - 🎥 Videos (.mp4, .avi, .mov)

- **Performance Analysis:**
  - Compression ratio measurement
  - Speed benchmarking
  - Space savings calculation
  - Automatic visualization generation

- **Interactive Jupyter Notebook:**
  - Step-by-step demonstrations
  - Visual comparisons
  - Educational examples

## 📁 Project Structure

```
DataCompressionProject/
├── algorithms/           # Compression algorithm implementations
│   ├── rle.py           # Run Length Encoding
│   ├── huffman.py       # Huffman Coding
│   └── lzw.py           # LZW Compression
├── handlers/            # File type handlers
│   ├── image_handler.py
│   ├── video_handler.py
│   └── document_handler.py
├── utils/               # Utility functions
│   ├── performance.py   # Performance measurement
│   └── visualization.py # Plotting and charts
├── compress.py          # Main CLI application
├── Compression_Analysis.ipynb  # Interactive notebook
├── output/              # Results and visualizations
└── sample_files/        # Test files
```

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Required Libraries

```bash
pip install numpy pandas matplotlib pillow opencv-python
```

### Optional (for document support)

```bash
pip install PyPDF2 python-docx
```

### Clone or Download

```bash
# Clone the repository or download the ZIP file
cd DataCompressionProject
```

## 💻 Usage

### Method 1: Command Line Interface

```bash
# Compress a file with all algorithms
python compress.py myfile.txt

# Use specific algorithm
python compress.py myimage.png --algorithm huffman

# Convert images/videos to grayscale
python compress.py video.mp4 --grayscale

# Specify output directory
python compress.py document.pdf --output results/
```

**Available Options:**
- `-a, --algorithm`: Choose compression algorithm (rle, huffman, lzw, all)
- `-g, --grayscale`: Convert images/videos to grayscale before compression
- `-o, --output`: Specify output directory for results

### Method 2: Jupyter Notebook

1. Open the notebook:
   ```bash
   jupyter notebook Compression_Analysis.ipynb
   ```

2. Run cells sequentially to:
   - Learn about each algorithm
   - Test on different data types
   - Compare performance metrics
   - Generate visualizations

### Method 3: Python API

```python
from algorithms import rle, huffman, lzw
from utils import performance

# Your data
text = "Hello World! " * 100
data = [ord(c) for c in text]

# Compress with RLE
compressed = rle.compress(data)
decompressed = rle.decompress(compressed)

# Compress with Huffman
encoded, codes = huffman.compress(text)
decoded = huffman.decompress(encoded, codes)

# Compress with LZW
compressed = lzw.compress(text)
decompressed = lzw.decompress(compressed)

# Performance comparison
algorithms = [
    ('RLE', rle.compress, rle.decompress, False),
    ('Huffman', huffman.compress, lambda c: huffman.decompress(c[0], c[1]), True),
    ('LZW', lzw.compress, lzw.decompress, False)
]
results = performance.compare_algorithms(data, algorithms)
performance.print_comparison_table(results)
```

## 📊 Example Output

```
================================================================================
  Compression Test - Sample Text
================================================================================

Algorithm       Orig Size    Comp Size    Ratio      Saving %   Comp Time    Decomp Time
================================================================================
RLE             5000         2500         0.5000     50.00      0.001234     0.000567
Huffman         5000         3200         0.6400     36.00      0.002345     0.001234
LZW             5000         3000         0.6000     40.00      0.001890     0.000890
================================================================================

📊 Best Performers:
   🏆 Best Compression Ratio: RLE (0.5000)
   ⚡ Fastest Compression: RLE (0.001234s)
   🔄 Fastest Decompression: RLE (0.000567s)
```

## 📈 Performance Metrics

The project measures:

- **Compression Ratio**: Compressed size / Original size (lower is better)
- **Space Savings**: Percentage of space saved
- **Compression Time**: Time taken to compress
- **Decompression Time**: Time taken to decompress
- **Correctness**: Verification that decompressed data matches original

## 🎓 Algorithm Comparison

| Algorithm | Best For | Speed | Compression | Use Case |
|-----------|----------|-------|-------------|----------|
| **RLE** | Repetitive data | ⚡⚡⚡ Very Fast | Good on repetitive, poor on random | Images, simple graphics |
| **Huffman** | Text with varying frequencies | ⚡⚡ Moderate | Optimal for frequency-based | Text files, general purpose |
| **LZW** | Patterns and dictionaries | ⚡⚡ Good | Good all-around | GIF, general compression |

## 📝 Examples

### Compress an Image

```bash
python compress.py photo.jpg --grayscale --output results/
```

Output:
- Performance comparison table
- Visualization charts (ratio, time, savings)
- JSON results file

### Compress a Document

```bash
python compress.py report.pdf --algorithm all
```

### Test Custom Text

Open `Compression_Analysis.ipynb` and use the interactive testing cell to input your own text.

## 🔧 Customization

### Add Your Own Algorithm

1. Create a new file in `algorithms/` directory
2. Implement `compress()` and `decompress()` functions
3. Add to the comparison in `compress.py`

### Extend File Type Support

1. Create a handler in `handlers/` directory
2. Implement `prepare_for_compression()` and `reconstruct()` functions
3. Add file extension mapping in `compress.py`

## 📚 Educational Content

The Jupyter notebook includes:
- Algorithm explanations with code
- Step-by-step demonstrations
- Visual comparisons
- Performance analysis
- Best practices and recommendations

## 🐛 Troubleshooting

**Issue:** ImportError for cv2 or PIL
- **Solution:** Install required packages: `pip install opencv-python pillow`

**Issue:** PDF/DOCX files not loading
- **Solution:** Install optional packages: `pip install PyPDF2 python-docx`

**Issue:** Memory error with large files
- **Solution:** Use `--grayscale` flag or process smaller sections

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Add new compression algorithms
- Improve performance
- Add support for more file types
- Enhance visualizations
- Fix bugs

## 📄 License

This project is licensed under the MIT License - feel free to use it for learning and development.

## 👨‍💻 Author

Data Compression Project - 2025

## 🌟 Acknowledgments

Based on classic compression algorithms:
- Run Length Encoding (RLE)
- Huffman Coding (David A. Huffman, 1952)
- LZW (Lempel, Ziv, Welch, 1984)

## 📞 Support

For questions or issues:
1. Check the Jupyter notebook for examples
2. Review the code documentation
3. Test with sample files in `sample_files/` directory

---

**Happy Compressing! 🚀**
