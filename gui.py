"""
Graphical User Interface for Data Compression Project
Interactive GUI to compress files and view results
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import sys
import os
import time
import threading
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from algorithms import rle, huffman, lzw


class CompressionGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Data Compression Project - Interactive GUI")
        self.root.geometry("1000x700")
        self.root.resizable(True, True)
        
        # Variables
        self.file_path = tk.StringVar()
        self.selected_algorithm = tk.StringVar(value="all")
        self.results = []
        
        # Create UI
        self.create_widgets()
        
        # Style
        self.setup_styles()
    
    def setup_styles(self):
        """Configure ttk styles."""
        style = ttk.Style()
        style.theme_use('default')
        
        # Configure colors
        style.configure('Title.TLabel', font=('Helvetica', 16, 'bold'), foreground='#2c3e50')
        style.configure('Header.TLabel', font=('Helvetica', 12, 'bold'), foreground='#34495e')
        style.configure('Info.TLabel', font=('Helvetica', 10), foreground='#7f8c8d')
        style.configure('Success.TLabel', font=('Helvetica', 10, 'bold'), foreground='#27ae60')
        style.configure('Error.TLabel', font=('Helvetica', 10, 'bold'), foreground='#e74c3c')
        
        style.configure('Action.TButton', font=('Helvetica', 10, 'bold'))
    
    def create_widgets(self):
        """Create all GUI widgets."""
        
        # Title Frame
        title_frame = ttk.Frame(self.root, padding="10")
        title_frame.pack(fill=tk.X)
        
        title = ttk.Label(
            title_frame, 
            text="🗜️ Data Compression Project", 
            style='Title.TLabel'
        )
        title.pack()
        
        subtitle = ttk.Label(
            title_frame,
            text="Compare RLE, Huffman, and LZW Algorithms",
            style='Info.TLabel'
        )
        subtitle.pack()
        
        ttk.Separator(self.root, orient='horizontal').pack(fill=tk.X, pady=10)
        
        # Input Frame
        input_frame = ttk.LabelFrame(self.root, text="📁 Input", padding="10")
        input_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # File selection
        file_frame = ttk.Frame(input_frame)
        file_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(file_frame, text="File:").pack(side=tk.LEFT, padx=5)
        
        file_entry = ttk.Entry(file_frame, textvariable=self.file_path, width=50)
        file_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        browse_btn = ttk.Button(
            file_frame, 
            text="Browse...", 
            command=self.browse_file,
            style='Action.TButton'
        )
        browse_btn.pack(side=tk.LEFT, padx=5)
        
        # Text input option
        text_frame = ttk.Frame(input_frame)
        text_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(text_frame, text="Or enter text directly:").pack(anchor=tk.W, padx=5)
        
        self.text_input = scrolledtext.ScrolledText(
            text_frame, 
            height=4, 
            width=70,
            font=('Courier', 10)
        )
        self.text_input.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)
        
        # Algorithm Selection Frame
        algo_frame = ttk.LabelFrame(self.root, text="⚙️ Algorithm Selection", padding="10")
        algo_frame.pack(fill=tk.X, padx=10, pady=5)
        
        algorithms = [
            ("All Algorithms", "all"),
            ("RLE (Run Length Encoding)", "rle"),
            ("Huffman Coding", "huffman"),
            ("LZW (Lempel-Ziv-Welch)", "lzw")
        ]
        
        for text, value in algorithms:
            rb = ttk.Radiobutton(
                algo_frame,
                text=text,
                variable=self.selected_algorithm,
                value=value
            )
            rb.pack(anchor=tk.W, pady=2)
        
        # Action Buttons
        button_frame = ttk.Frame(self.root, padding="10")
        button_frame.pack(fill=tk.X)
        
        compress_btn = ttk.Button(
            button_frame,
            text="🗜️ Compress & Analyze",
            command=self.start_compression,
            style='Action.TButton'
        )
        compress_btn.pack(side=tk.LEFT, padx=5)
        
        clear_btn = ttk.Button(
            button_frame,
            text="🗑️ Clear Results",
            command=self.clear_results
        )
        clear_btn.pack(side=tk.LEFT, padx=5)
        
        help_btn = ttk.Button(
            button_frame,
            text="❓ Help",
            command=self.show_help
        )
        help_btn.pack(side=tk.LEFT, padx=5)
        
        # Progress Bar
        self.progress = ttk.Progressbar(
            self.root,
            mode='indeterminate',
            length=200
        )
        self.progress.pack(fill=tk.X, padx=10, pady=5)
        
        # Status Label
        self.status_label = ttk.Label(
            self.root,
            text="Ready to compress",
            style='Info.TLabel'
        )
        self.status_label.pack(pady=5)
        
        ttk.Separator(self.root, orient='horizontal').pack(fill=tk.X, pady=10)
        
        # Results Frame
        results_frame = ttk.LabelFrame(self.root, text="📊 Results", padding="10")
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Results Text Area
        self.results_text = scrolledtext.ScrolledText(
            results_frame,
            height=15,
            width=100,
            font=('Courier', 9),
            bg='#f8f9fa',
            fg='#2c3e50'
        )
        self.results_text.pack(fill=tk.BOTH, expand=True)
        
        # Configure text tags for colored output
        self.results_text.tag_config('header', font=('Courier', 10, 'bold'), foreground='#2c3e50')
        self.results_text.tag_config('success', foreground='#27ae60', font=('Courier', 9, 'bold'))
        self.results_text.tag_config('warning', foreground='#f39c12', font=('Courier', 9, 'bold'))
        self.results_text.tag_config('error', foreground='#e74c3c', font=('Courier', 9, 'bold'))
        self.results_text.tag_config('info', foreground='#3498db', font=('Courier', 9, 'bold'))
    
    def browse_file(self):
        """Open file dialog to select a file."""
        filename = filedialog.askopenfilename(
            title="Select a file to compress",
            filetypes=[
                ("Text files", "*.txt"),
                ("All files", "*.*")
            ]
        )
        if filename:
            self.file_path.set(filename)
            self.text_input.delete('1.0', tk.END)  # Clear text input
    
    def clear_results(self):
        """Clear the results text area."""
        self.results_text.delete('1.0', tk.END)
        self.status_label.config(text="Ready to compress")
        self.results = []
    
    def show_help(self):
        """Show help dialog."""
        help_text = """
📖 Data Compression Project - Help

HOW TO USE:
1. Choose input method:
   • Browse for a file, OR
   • Enter text directly in the text box

2. Select algorithm:
   • All Algorithms - Compare all three
   • RLE - Best for repetitive data
   • Huffman - Best for text with varied frequencies
   • LZW - Best for patterns and general use

3. Click "Compress & Analyze"

4. View results showing:
   • Compression ratio
   • Space savings
   • Speed metrics
   • Best performer

ALGORITHM GUIDE:
• RLE: Fast, great for AAABBBBCCCC type data
• Huffman: Optimal for frequency-based compression
• LZW: Adaptive, used in GIF and general compression

TIP: Larger files compress better!
        """
        messagebox.showinfo("Help", help_text)
    
    def start_compression(self):
        """Start compression in a separate thread."""
        # Get input
        file_path = self.file_path.get()
        text_input = self.text_input.get('1.0', tk.END).strip()
        
        if not file_path and not text_input:
            messagebox.showwarning("No Input", "Please select a file or enter text to compress.")
            return
        
        # Start compression in thread to keep GUI responsive
        thread = threading.Thread(target=self.run_compression, daemon=True)
        thread.start()
    
    def run_compression(self):
        """Run compression (called in separate thread)."""
        try:
            # Update UI
            self.root.after(0, self.progress.start)
            self.root.after(0, lambda: self.status_label.config(text="Compressing..."))
            
            # Get data
            file_path = self.file_path.get()
            text_input = self.text_input.get('1.0', tk.END).strip()
            
            if file_path and os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    data_str = f.read()
                source = f"File: {os.path.basename(file_path)}"
            else:
                data_str = text_input
                source = "Direct Text Input"
            
            if not data_str:
                raise ValueError("No data to compress")
            
            data_list = [ord(c) for c in data_str]
            
            # Clear previous results
            self.root.after(0, lambda: self.results_text.delete('1.0', tk.END))
            
            # Print header
            self.print_result("=" * 90 + "\n", 'header')
            self.print_result(f"  COMPRESSION ANALYSIS\n", 'header')
            self.print_result("=" * 90 + "\n\n", 'header')
            self.print_result(f"Source: {source}\n", 'info')
            self.print_result(f"Size: {len(data_str):,} characters\n", 'info')
            self.print_result(f"Preview: {data_str[:100]}...\n\n" if len(data_str) > 100 else f"Content: {data_str}\n\n", 'info')
            
            # Get selected algorithms
            algo_choice = self.selected_algorithm.get()
            results = []
            
            if algo_choice in ['all', 'rle']:
                result = self.test_algorithm("RLE", rle.compress, rle.decompress, data_list, data_str, is_rle=True)
                results.append(result)
            
            if algo_choice in ['all', 'huffman']:
                result = self.test_algorithm("Huffman", huffman.compress, huffman.decompress, data_list, data_str, is_huffman=True)
                results.append(result)
            
            if algo_choice in ['all', 'lzw']:
                result = self.test_algorithm("LZW", lzw.compress, lzw.decompress, data_list, data_str)
                results.append(result)
            
            # Print summary
            self.print_summary(results)
            
            # Update status
            self.root.after(0, lambda: self.status_label.config(text="✅ Compression complete!"))
            
        except Exception as e:
            self.print_result(f"\n❌ Error: {str(e)}\n", 'error')
            self.root.after(0, lambda: self.status_label.config(text=f"Error: {str(e)}"))
        
        finally:
            self.root.after(0, self.progress.stop)
    
    def test_algorithm(self, name, compress_func, decompress_func, data_list, data_str, is_rle=False, is_huffman=False):
        """Test a single algorithm."""
        self.print_result(f"\n{'─' * 90}\n", 'header')
        self.print_result(f"Testing {name}\n", 'header')
        self.print_result(f"{'─' * 90}\n", 'header')
        
        # Choose data format
        if is_rle:
            test_data = data_list
        else:
            test_data = data_str
        
        # Compress
        start = time.time()
        compressed = compress_func(test_data)
        comp_time = time.time() - start
        
        # Get size
        if is_huffman:
            encoded, codes = compressed
            comp_size = len(encoded)
        elif is_rle:
            comp_size = len(compressed) * 2
        else:
            comp_size = len(str(compressed))
        
        # Decompress
        start = time.time()
        if is_huffman:
            decompressed = decompress_func(encoded, codes)
        else:
            decompressed = decompress_func(compressed)
        decomp_time = time.time() - start
        
        # Calculate metrics
        orig_size = len(data_str)
        ratio = comp_size / orig_size if orig_size > 0 else 1
        space_saving = ((orig_size - comp_size) / orig_size * 100) if orig_size > 0 else 0
        
        # Verify
        if is_huffman:
            is_correct = ''.join(decompressed) == data_str
        elif is_rle:
            is_correct = list(decompressed) == data_list
        else:
            is_correct = decompressed == data_str
        
        # Print results
        self.print_result(f"Original Size:       {orig_size:>10,} bytes\n")
        self.print_result(f"Compressed Size:     {comp_size:>10,} bytes\n")
        self.print_result(f"Compression Ratio:   {ratio:>10.4f}\n")
        
        if space_saving >= 0:
            self.print_result(f"Space Savings:       {space_saving:>9.2f}%\n", 'success')
        else:
            self.print_result(f"Space Savings:       {space_saving:>9.2f}% (EXPANDED)\n", 'warning')
        
        self.print_result(f"Compression Time:    {comp_time:>10.6f} seconds\n")
        self.print_result(f"Decompression Time:  {decomp_time:>10.6f} seconds\n")
        self.print_result(f"Verification:        ", '')
        
        if is_correct:
            self.print_result("✓ PASSED\n", 'success')
        else:
            self.print_result("✗ FAILED\n", 'error')
        
        return {
            'name': name,
            'ratio': ratio,
            'saving': space_saving,
            'comp_time': comp_time,
            'decomp_time': decomp_time,
            'correct': is_correct
        }
    
    def print_summary(self, results):
        """Print summary of all results."""
        self.print_result(f"\n\n{'=' * 90}\n", 'header')
        self.print_result("  📊 SUMMARY - BEST PERFORMERS\n", 'header')
        self.print_result(f"{'=' * 90}\n\n", 'header')
        
        if not results:
            return
        
        # Best compression
        valid_results = [r for r in results if r['saving'] > 0]
        if valid_results:
            best_ratio = min(valid_results, key=lambda x: x['ratio'])
            self.print_result(f"🏆 Best Compression Ratio:   {best_ratio['name']} ", 'success')
            self.print_result(f"(saved {best_ratio['saving']:.2f}%)\n", 'success')
        else:
            self.print_result("⚠️  No algorithm achieved compression (all expanded data)\n", 'warning')
            self.print_result("   TIP: Try larger files or more repetitive/patterned data\n", 'info')
        
        # Fastest compression
        fastest = min(results, key=lambda x: x['comp_time'])
        self.print_result(f"⚡ Fastest Compression:      {fastest['name']} ", 'info')
        self.print_result(f"({fastest['comp_time']:.6f}s)\n", 'info')
        
        # Fastest decompression
        fastest_d = min(results, key=lambda x: x['decomp_time'])
        self.print_result(f"🔄 Fastest Decompression:    {fastest_d['name']} ", 'info')
        self.print_result(f"({fastest_d['decomp_time']:.6f}s)\n", 'info')
        
        # Algorithm recommendations
        self.print_result("\n💡 Recommendations:\n", 'info')
        for result in results:
            if result['saving'] > 0:
                self.print_result(f"   • {result['name']}: Good choice for this data type\n", 'success')
            else:
                self.print_result(f"   • {result['name']}: Not suitable for this data\n", 'warning')
    
    def print_result(self, text, tag=''):
        """Print text to results area with optional tag."""
        def _print():
            if tag:
                self.results_text.insert(tk.END, text, tag)
            else:
                self.results_text.insert(tk.END, text)
            self.results_text.see(tk.END)
        
        self.root.after(0, _print)


def main():
    """Main entry point."""
    root = tk.Tk()
    app = CompressionGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
