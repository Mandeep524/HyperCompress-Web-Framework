# Quick Start Guide

## Getting Started in 5 Minutes

### 1. Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

### 2. Quick Test

#### Using the Jupyter Notebook (Recommended for beginners)
```bash
jupyter notebook Compression_Analysis.ipynb
```
Then run all cells to see examples.

#### Using Command Line
```bash
# Test with sample file
python compress.py sample_files/sample_text.txt

# Test with your own file
python compress.py /path/to/your/file.txt
```

### 3. Understanding the Output

After running compression, you'll see:
- **Comparison Table**: Shows performance metrics for each algorithm
- **Best Performers**: Highlights which algorithm works best
- **Visualizations**: Charts saved in `output/` directory

### 4. Next Steps

- Explore the Jupyter notebook for interactive examples
- Try different file types (images, PDFs, videos)
- Experiment with the `--algorithm` flag to test individual algorithms
- Check the `example.py` file for API usage

## Common Commands

```bash
# Compress with specific algorithm
python compress.py myfile.txt --algorithm huffman

# Convert images to grayscale before compression
python compress.py image.jpg --grayscale

# Save results to custom directory
python compress.py data.csv --output my_results/

# Get help
python compress.py --help
```

## Tips

- **Large files**: Use `--grayscale` for images/videos to reduce processing time
- **Best compression**: Try all algorithms with `--algorithm all` (default)
- **Learning**: Start with the Jupyter notebook for step-by-step explanations

## Need Help?

1. Check README.md for detailed documentation
2. Review example.py for code samples
3. Open Compression_Analysis.ipynb for tutorials
