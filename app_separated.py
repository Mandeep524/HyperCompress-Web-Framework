"""
Data Compression Project - Separated Web Application
Each file type (Image, Video, Document) has its own dedicated page
Each algorithm (RLE, Huffman, LZW) has its own set of routes
"""

from flask import Flask, render_template_string, request, jsonify, send_file
import sys
import os
import io
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

# Import blueprints
from routes import rle_bp, huffman_bp, lzw_bp

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max
app.config['SECRET_KEY'] = 'compression_project_separated_2025'

# Register blueprints
app.register_blueprint(rle_bp)
app.register_blueprint(huffman_bp)
app.register_blueprint(lzw_bp)

# Create necessary directories
os.makedirs('uploads', exist_ok=True)
os.makedirs('compressed', exist_ok=True)

# Common CSS for all pages
COMMON_CSS = """
<style>
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    :root {
        --bg-gradient-start: #667eea;
        --bg-gradient-end: #764ba2;
        --container-bg: white;
        --text-color: #333;
        --section-bg: #f8f9fa;
        --border-color: #e0e0e0;
        --card-bg: white;
        --primary-color: #667eea;
        --secondary-color: #764ba2;
    }
    
    body.dark-mode {
        --bg-gradient-start: #1a1a2e;
        --bg-gradient-end: #16213e;
        --container-bg: #0f3460;
        --text-color: #e0e0e0;
        --section-bg: #1a1a2e;
        --border-color: #2d3561;
        --card-bg: #16213e;
        --primary-color: #5bc0de;
        --secondary-color: #9b59b6;
    }
    
    body {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        background: linear-gradient(135deg, var(--bg-gradient-start) 0%, var(--bg-gradient-end) 100%);
        min-height: 100vh;
        padding: 20px;
        color: var(--text-color);
        transition: all 0.3s ease;
    }
    
    .dark-mode-toggle {
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 1000;
        padding: 12px 20px;
        background: rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(10px);
        border: 2px solid rgba(255, 255, 255, 0.3);
        border-radius: 50px;
        cursor: pointer;
        font-size: 24px;
        transition: all 0.3s;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .dark-mode-toggle:hover {
        transform: scale(1.1);
        background: rgba(255, 255, 255, 0.3);
    }
    
    .container {
        max-width: 1400px;
        margin: 0 auto;
        background: var(--container-bg);
        border-radius: 15px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        overflow: hidden;
        transition: all 0.3s ease;
    }
    
    .header {
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
        color: white;
        padding: 30px;
        text-align: center;
    }
    
    .header h1 {
        font-size: 2.5em;
        margin-bottom: 10px;
    }
    
    .header p {
        font-size: 1.1em;
        opacity: 0.9;
    }
    
    .nav-bar {
        display: flex;
        justify-content: center;
        gap: 20px;
        padding: 20px;
        background: var(--section-bg);
        border-bottom: 2px solid var(--border-color);
        flex-wrap: wrap;
    }
    
    .nav-button {
        padding: 12px 30px;
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
        color: white;
        border: none;
        border-radius: 8px;
        cursor: pointer;
        font-size: 16px;
        text-decoration: none;
        transition: all 0.3s;
        display: inline-block;
    }
    
    .nav-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    
    .nav-button.active {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    }
    
    .content {
        padding: 30px;
    }
    
    .section {
        margin-bottom: 30px;
        padding: 25px;
        background: var(--section-bg);
        border-radius: 10px;
    }
    
    .section-title {
        font-size: 1.5em;
        color: var(--primary-color);
        margin-bottom: 20px;
        padding-bottom: 10px;
        border-bottom: 2px solid var(--border-color);
    }
    
    .upload-area {
        border: 3px dashed var(--primary-color);
        border-radius: 10px;
        padding: 40px;
        text-align: center;
        background: var(--card-bg);
        cursor: pointer;
        transition: all 0.3s;
    }
    
    .upload-area:hover {
        border-color: var(--secondary-color);
        background: var(--section-bg);
    }
    
    .upload-area input[type="file"] {
        display: none;
    }
    
    .upload-icon {
        font-size: 48px;
        margin-bottom: 15px;
    }
    
    .algorithm-buttons {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 15px;
        margin-top: 20px;
    }
    
    .algo-button {
        padding: 15px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        cursor: pointer;
        font-size: 16px;
        transition: all 0.3s;
    }
    
    .algo-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    
    .algo-button:disabled {
        opacity: 0.5;
        cursor: not-allowed;
    }
    
    .results-area {
        margin-top: 30px;
        display: none;
    }
    
    .results-area.show {
        display: block;
    }
    
    .result-card {
        background: white;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 15px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    
    .result-header {
        font-size: 1.3em;
        color: #667eea;
        margin-bottom: 15px;
        padding-bottom: 10px;
        border-bottom: 2px solid #f0f0f0;
    }
    
    .metrics-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 15px;
        margin-top: 15px;
    }
    
    .metric-item {
        padding: 15px;
        background: #f8f9fa;
        border-radius: 8px;
        text-align: center;
    }
    
    .metric-label {
        font-size: 0.9em;
        color: #666;
        margin-bottom: 5px;
    }
    
    .metric-value {
        font-size: 1.5em;
        font-weight: bold;
        color: #667eea;
    }
    
    .success {
        color: #28a745;
    }
    
    .error {
        color: #dc3545;
    }
    
    .loading {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid #f3f3f3;
        border-top: 3px solid #667eea;
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .checkbox-container {
        margin: 20px 0;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .checkbox-container input[type="checkbox"] {
        width: 20px;
        height: 20px;
        cursor: pointer;
    }
    
    .checkbox-container label {
        font-size: 16px;
        cursor: pointer;
    }
</style>
"""

# Home page
HOME_PAGE = COMMON_CSS + """
<style>
    .algo-card {
        padding: 20px;
        background: var(--card-bg);
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        cursor: pointer;
        transition: all 0.3s;
    }
    
    body.dark-mode .algo-card {
        box-shadow: 0 2px 10px rgba(0,0,0,0.5);
    }
    
    .algo-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 5px 20px rgba(0,0,0,0.15);
    }
    
    body.dark-mode .algo-card:hover {
        box-shadow: 0 5px 20px rgba(0,0,0,0.6);
    }
    
    .algo-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 10px;
    }
    
    .algo-title {
        color: #667eea;
        margin: 0;
    }
    
    .expand-icon {
        font-size: 24px;
        transition: transform 0.3s;
    }
    
    .expand-icon.expanded {
        transform: rotate(180deg);
    }
    
    .algo-brief {
        color: #666;
        margin: 10px 0;
    }
    
    .algo-details {
        max-height: 0;
        overflow: hidden;
        transition: max-height 0.3s ease-out;
        color: #555;
    }
    
    .algo-details.show {
        max-height: 800px;
        transition: max-height 0.5s ease-in;
    }
    
    .algo-details h5 {
        color: #764ba2;
        margin-top: 15px;
        margin-bottom: 8px;
    }
    
    .algo-details ul {
        margin-left: 20px;
        line-height: 1.8;
    }
    
    .algo-details p {
        line-height: 1.6;
        margin: 10px 0;
    }
</style>

<button class="dark-mode-toggle" onclick="toggleDarkMode()" title="Toggle Dark Mode">🌙</button>

<div class="container">
    <div class="header">
        <h1>🗜️ Data Compression Project</h1>
        <p>Choose a file type to compress</p>
    </div>
    
    <div class="nav-bar">
        <a href="/" class="nav-button active">🏠 Home</a>
        <a href="/text" class="nav-button">📝 Text</a>
        <a href="/images" class="nav-button">🖼️ Images</a>
        <a href="/videos" class="nav-button">🎥 Videos</a>
        <a href="/documents" class="nav-button">📄 Documents</a>
        <a href="/decompress" class="nav-button">🔓 Decompress</a>
        <a href="/history" class="nav-button">📊 History</a>
    </div>
    
    <div class="content">
        <h2 style="color: var(--primary-color); margin-bottom: 20px;">Welcome to the Data Compression Project</h2>
        
        <div class="section">
            <h3 style="color: #764ba2; margin-bottom: 15px;">Available Compression Algorithms (Click to Learn More)</h3>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px;">
                
                <!-- RLE Algorithm -->
                <div class="algo-card" onclick="toggleAlgo('rle')">
                    <div class="algo-header">
                        <h4 class="algo-title">🔄 RLE (Run Length Encoding)</h4>
                        <span class="expand-icon" id="rle-icon">▼</span>
                    </div>
                    <p class="algo-brief">Best for data with repetitive patterns. Fast and simple compression algorithm.</p>
                    <div class="algo-details" id="rle-details">
                        <h5>📋 How It Works:</h5>
                        <p>RLE replaces sequences of identical data values with a single value and count. For example, "AAAABBBCCC" becomes "4A3B3C".</p>
                        
                        <h5>✅ Advantages:</h5>
                        <ul>
                            <li>Extremely fast compression and decompression</li>
                            <li>Very simple to implement</li>
                            <li>Low memory requirements</li>
                            <li>Excellent for data with long runs of repeated values</li>
                        </ul>
                        
                        <h5>❌ Limitations:</h5>
                        <ul>
                            <li>Can increase file size if data has no repetitions</li>
                            <li>Not ideal for random or highly variable data</li>
                            <li>Less effective than modern algorithms for general use</li>
                        </ul>
                        
                        <h5>🎯 Best Use Cases:</h5>
                        <ul>
                            <li>Simple graphics and icons</li>
                            <li>Fax transmissions</li>
                            <li>Data with long repetitive sequences</li>
                            <li>Real-time compression needs</li>
                        </ul>
                    </div>
                </div>
                
                <!-- Huffman Coding -->
                <div class="algo-card" onclick="toggleAlgo('huffman')">
                    <div class="algo-header">
                        <h4 class="algo-title">🌳 Huffman Coding</h4>
                        <span class="expand-icon" id="huffman-icon">▼</span>
                    </div>
                    <p class="algo-brief">Optimal for text with varying character frequencies. Variable-length encoding.</p>
                    <div class="algo-details" id="huffman-details">
                        <h5>📋 How It Works:</h5>
                        <p>Huffman creates a binary tree based on character frequency. More frequent characters get shorter codes, less frequent ones get longer codes.</p>
                        
                        <h5>✅ Advantages:</h5>
                        <ul>
                            <li>Optimal prefix-free code</li>
                            <li>No information loss (lossless)</li>
                            <li>Highly effective for text compression</li>
                            <li>Adapts to data statistics</li>
                            <li>Used in JPEG, MP3, and ZIP formats</li>
                        </ul>
                        
                        <h5>❌ Limitations:</h5>
                        <ul>
                            <li>Requires two passes (frequency analysis + encoding)</li>
                            <li>Must store or transmit the frequency table</li>
                            <li>Not effective on small files</li>
                            <li>Fixed encoding for entire file</li>
                        </ul>
                        
                        <h5>🎯 Best Use Cases:</h5>
                        <ul>
                            <li>Text file compression</li>
                            <li>Part of DEFLATE algorithm (ZIP, GZIP)</li>
                            <li>JPEG image compression</li>
                            <li>Data with varying symbol frequencies</li>
                        </ul>
                    </div>
                </div>
                
                <!-- LZW Algorithm -->
                <div class="algo-card" onclick="toggleAlgo('lzw')">
                    <div class="algo-header">
                        <h4 class="algo-title">📚 LZW (Lempel-Ziv-Welch)</h4>
                        <span class="expand-icon" id="lzw-icon">▼</span>
                    </div>
                    <p class="algo-brief">Dictionary-based compression. Great for general-purpose compression.</p>
                    <div class="algo-details" id="lzw-details">
                        <h5>📋 How It Works:</h5>
                        <p>LZW builds a dictionary of patterns as it compresses. It replaces repeated patterns with references to dictionary entries, adapting to the data dynamically.</p>
                        
                        <h5>✅ Advantages:</h5>
                        <ul>
                            <li>Single-pass algorithm (fast)</li>
                            <li>No need to store dictionary (rebuilt during decompression)</li>
                            <li>Adapts to changing data patterns</li>
                            <li>Good compression ratios for most data types</li>
                            <li>Universal compression algorithm</li>
                        </ul>
                        
                        <h5>❌ Limitations:</h5>
                        <ul>
                            <li>Dictionary size can grow large</li>
                            <li>Less efficient than modern algorithms (Bzip2, LZMA)</li>
                            <li>Performance depends on data patterns</li>
                            <li>Patent issues (expired in 2004)</li>
                        </ul>
                        
                        <h5>🎯 Best Use Cases:</h5>
                        <ul>
                            <li>GIF image compression</li>
                            <li>TIFF image format</li>
                            <li>PDF files</li>
                            <li>Unix compress utility</li>
                            <li>General purpose file compression</li>
                        </ul>
                    </div>
                </div>
                
            </div>
        </div>

<script>
function toggleAlgo(algoName) {
    const details = document.getElementById(algoName + '-details');
    const icon = document.getElementById(algoName + '-icon');
    
    details.classList.toggle('show');
    icon.classList.toggle('expanded');
}

function toggleDarkMode() {
    document.body.classList.toggle('dark-mode');
    const isDark = document.body.classList.contains('dark-mode');
    localStorage.setItem('darkMode', isDark);
    document.querySelector('.dark-mode-toggle').textContent = isDark ? '☀️' : '🌙';
}

// Load saved dark mode preference
if(localStorage.getItem('darkMode') === 'true') {
    document.body.classList.add('dark-mode');
    document.querySelector('.dark-mode-toggle').textContent = '☀️';
}
</script>
        
        <div class="section">
            <h3 style="color: var(--secondary-color); margin-bottom: 15px;">Supported File Types</h3>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px;">
                <div style="padding: 20px; background: var(--card-bg); border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                    <h4 style="color: var(--primary-color); margin-bottom: 10px;">📝 Text</h4>
                    <p style="color: var(--text-color);">Direct text input for instant compression</p>
                    <a href="/text" style="display: inline-block; margin-top: 10px; color: var(--primary-color); text-decoration: none; font-weight: bold;">Compress Text →</a>
                </div>
                <div style="padding: 20px; background: var(--card-bg); border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                    <h4 style="color: var(--primary-color); margin-bottom: 10px;">🖼️ Images</h4>
                    <p style="color: var(--text-color);">PNG, JPG, JPEG, BMP, GIF formats supported</p>
                    <a href="/images" style="display: inline-block; margin-top: 10px; color: var(--primary-color); text-decoration: none; font-weight: bold;">Compress Images →</a>
                </div>
                <div style="padding: 20px; background: var(--card-bg); border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                    <h4 style="color: var(--primary-color); margin-bottom: 10px;">🎥 Videos</h4>
                    <p style="color: var(--text-color);">MP4, AVI, MOV formats supported</p>
                    <a href="/videos" style="display: inline-block; margin-top: 10px; color: var(--primary-color); text-decoration: none; font-weight: bold;">Compress Videos →</a>
                </div>
                <div style="padding: 20px; background: var(--card-bg); border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                    <h4 style="color: var(--primary-color); margin-bottom: 10px;">📄 Documents</h4>
                    <p style="color: var(--text-color);">TXT, PDF, DOCX, CSV formats supported</p>
                    <a href="/documents" style="display: inline-block; margin-top: 10px; color: var(--primary-color); text-decoration: none; font-weight: bold;">Compress Documents →</a>
                </div>
                <div style="padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 10px; box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3); color: white;">
                    <h4 style="color: white; margin-bottom: 10px;">🔓 Decompress</h4>
                    <p style="color: rgba(255, 255, 255, 0.95);">Upload .pkl files to restore original data</p>
                    <a href="/decompress" style="display: inline-block; margin-top: 10px; color: white; text-decoration: none; font-weight: bold; background: rgba(255, 255, 255, 0.2); padding: 5px 15px; border-radius: 5px;">Decompress Files →</a>
                </div>
            </div>
        </div>
        
        <div class="section">
            <h3 style="color: var(--secondary-color); margin-bottom: 15px;">📊 Performance Metrics</h3>
            <p style="color: var(--text-color); line-height: 1.6;">
                For each compression operation, we provide detailed metrics including:
                compression ratio, space savings percentage, compression time, 
                decompression time, and data integrity verification.
            </p>
        </div>
    </div>
</div>
"""

# Image compression page
IMAGE_PAGE = COMMON_CSS + """
<button class="dark-mode-toggle" onclick="toggleDarkMode()" title="Toggle Dark Mode">🌙</button>

<div class="container">
    <div class="header">
        <h1>🖼️ Image Compression</h1>
        <p>Upload an image and compress it with different algorithms</p>
    </div>
    
    <div class="nav-bar">
        <a href="/" class="nav-button">🏠 Home</a>
        <a href="/text" class="nav-button">📝 Text</a>
        <a href="/images" class="nav-button active">🖼️ Images</a>
        <a href="/videos" class="nav-button">🎥 Videos</a>
        <a href="/documents" class="nav-button">📄 Documents</a>
        <a href="/decompress" class="nav-button">🔓 Decompress</a>
        <a href="/history" class="nav-button">📊 History</a>
    </div>
    
    <div class="content">
        <!-- Compression Expectations Banner -->
        <div class="section" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; margin-bottom: 20px; border-radius: 15px; box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);">
            <h3 style="margin: 0 0 15px 0; font-size: 1.3em;">💡 Understanding Image Compression</h3>
            <div style="background: rgba(255, 255, 255, 0.15); padding: 15px; border-radius: 10px; margin-bottom: 10px;">
                <p style="margin: 0 0 10px 0; font-size: 0.95em;"><strong>🎯 What to expect:</strong></p>
                <ul style="margin: 5px 0; padding-left: 20px; font-size: 0.9em;">
                    <li><strong>Simple graphics</strong> (logos, icons, drawings): ✅ <strong>Excellent compression!</strong></li>
                    <li><strong>Screenshots & text</strong>: ✅ <strong>Good compression</strong></li>
                    <li><strong>Photos & complex images</strong>: ⚠️ <strong>Limited compression</strong> (this is normal!)</li>
                </ul>
            </div>
            <div style="background: rgba(255, 255, 255, 0.15); padding: 15px; border-radius: 10px;">
                <p style="margin: 0 0 8px 0; font-size: 0.95em;"><strong>⭐ Tips for better results:</strong></p>
                <p style="margin: 0; font-size: 0.9em;">✅ Check "Convert to grayscale" (reduces data by 3x)<br>
                ✅ Try simple images or screenshots<br>
                ✅ LZW usually works best for images<br>
                ⚠️ Photos don't compress well with these algorithms (they're designed for text!)</p>
            </div>
        </div>
        
        <div class="section">
            <h3 class="section-title">Upload Image</h3>
            <div class="upload-area" id="uploadArea">
                <div class="upload-icon">📤</div>
                <h3>Click to upload or drag and drop</h3>
                <p>Supported formats: PNG, JPG, JPEG, BMP, GIF</p>
                <input type="file" id="fileInput" accept=".png,.jpg,.jpeg,.bmp,.gif">
            </div>
            
            <div class="checkbox-container">
                <input type="checkbox" id="grayscale">
                <label for="grayscale">Convert to grayscale before compression</label>
            </div>
            
            <div class="checkbox-container" style="margin-top: 10px;">
                <label for="resizeOption" style="margin-right: 10px;">Resize image:</label>
                <select id="resizeOption" style="padding: 8px; border-radius: 5px; border: 1px solid #ccc; background: white; cursor: pointer;">
                    <option value="none">Original size (may be slow for large images)</option>
                    <option value="75">75% of original size</option>
                    <option value="50" selected>50% of original size (Recommended)</option>
                    <option value="25">25% of original size (Fast)</option>
                </select>
            </div>
            
            <div id="fileInfo" style="margin-top: 20px; display: none;">
                <p><strong>Selected file:</strong> <span id="fileName"></span></p>
                <p><strong>File size:</strong> <span id="fileSize"></span></p>
                <p id="largeSizeWarning" style="color: #ff6b6b; font-weight: bold; display: none;">
                    ⚠️ Large file detected! Consider using 50% or 25% resize for faster compression.
                </p>
            </div>
            
            <div class="algorithm-buttons">
                <button class="algo-button" onclick="compressImage('rle')" id="rleBtn" disabled>
                    🔄 Compress with RLE
                </button>
                <button class="algo-button" onclick="compressImage('huffman')" id="huffmanBtn" disabled>
                    🌳 Compress with Huffman
                </button>
                <button class="algo-button" onclick="compressImage('lzw')" id="lzwBtn" disabled>
                    📚 Compress with LZW
                </button>
                <button class="algo-button" onclick="compressImageAll()" id="allBtn" disabled>
                    ⚡ Compare All Algorithms
                </button>
            </div>
        </div>
        
        <div class="results-area" id="resultsArea">
            <h3 class="section-title">Compression Results</h3>
            <div id="resultsContent"></div>
        </div>
    </div>
</div>

<script>
let selectedFile = null;

const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const fileInfo = document.getElementById('fileInfo');
const fileName = document.getElementById('fileName');
const fileSize = document.getElementById('fileSize');
const buttons = ['rleBtn', 'huffmanBtn', 'lzwBtn', 'allBtn'];

// Click to upload
uploadArea.addEventListener('click', () => fileInput.click());

// File input change
fileInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        handleFile(e.target.files[0]);
    }
});

// Drag and drop functionality
uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    e.stopPropagation();
    uploadArea.style.borderColor = '#764ba2';
    uploadArea.style.background = '#f0f0ff';
});

uploadArea.addEventListener('dragleave', (e) => {
    e.preventDefault();
    e.stopPropagation();
    uploadArea.style.borderColor = '#667eea';
    uploadArea.style.background = 'white';
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    e.stopPropagation();
    uploadArea.style.borderColor = '#667eea';
    uploadArea.style.background = 'white';
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFile(files[0]);
    }
});

function handleFile(file) {
    selectedFile = file;
    fileName.textContent = selectedFile.name;
    const fileSizeKB = selectedFile.size / 1024;
    fileSize.textContent = fileSizeKB.toFixed(2) + ' KB';
    fileInfo.style.display = 'block';
    
    // Show warning for large files (>1MB)
    const largeSizeWarning = document.getElementById('largeSizeWarning');
    if (fileSizeKB > 1024) {
        largeSizeWarning.style.display = 'block';
    } else {
        largeSizeWarning.style.display = 'none';
    }
    
    buttons.forEach(id => document.getElementById(id).disabled = false);
}

async function compressImage(algorithm) {
    if (!selectedFile) return;
    
    const formData = new FormData();
    formData.append('file', selectedFile);
    formData.append('grayscale', document.getElementById('grayscale').checked);
    
    // Add resize option
    const resizeOption = document.getElementById('resizeOption').value;
    if (resizeOption !== 'none') {
        formData.append('resize', resizeOption);
    }
    
    const resultsArea = document.getElementById('resultsArea');
    const resultsContent = document.getElementById('resultsContent');
    
    resultsArea.classList.add('show');
    resultsContent.innerHTML = '<div class="loading"></div> Compressing with ' + algorithm.toUpperCase() + '...';
    
    try {
        const response = await fetch(`/${algorithm}/compress/image`, {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (data.error) {
            resultsContent.innerHTML = `<div class="error">Error: ${data.error}</div>`;
        } else {
            displayResult(data);
        }
    } catch (error) {
        resultsContent.innerHTML = `<div class="error">Error: ${error.message}</div>`;
    }
}

async function compressImageAll() {
    if (!selectedFile) return;
    
    const resultsArea = document.getElementById('resultsArea');
    const resultsContent = document.getElementById('resultsContent');
    
    resultsArea.classList.add('show');
    resultsContent.innerHTML = '<div class="loading"></div> Compressing with all algorithms...';
    
    const algorithms = ['rle', 'huffman', 'lzw'];
    const results = [];
    
    for (const algo of algorithms) {
        const formData = new FormData();
        formData.append('file', selectedFile);
        formData.append('grayscale', document.getElementById('grayscale').checked);
        
        // Add resize option
        const resizeOption = document.getElementById('resizeOption').value;
        if (resizeOption !== 'none') {
            formData.append('resize', resizeOption);
        }
        
        try {
            const response = await fetch(`/${algo}/compress/image`, {
                method: 'POST',
                body: formData
            });
            const data = await response.json();
            results.push(data);
        } catch (error) {
            results.push({ algorithm: algo, error: error.message });
        }
    }
    
    displayComparison(results);
}

function displayResult(data) {
    const resultsContent = document.getElementById('resultsContent');
    
    resultsContent.innerHTML = `
        <div class="result-card">
            <div class="result-header">${data.algorithm} Compression Results</div>
            <div class="metrics-grid">
                <div class="metric-item">
                    <div class="metric-label">Original Size</div>
                    <div class="metric-value">${(data.original_size / 1024).toFixed(2)} KB</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">Compressed Data Size</div>
                    <div class="metric-value">${(data.compressed_size / 1024).toFixed(2)} KB</div>
                </div>
                ${data.actual_file_size ? `
                <div class="metric-item" style="background: #fff3cd; border-left: 3px solid #ffc107;">
                    <div class="metric-label">⬇️ Download Size</div>
                    <div class="metric-value" style="color: #856404; font-weight: bold;">${(data.actual_file_size / 1024).toFixed(2)} KB</div>
                </div>
                ` : ''}
                <div class="metric-item">
                    <div class="metric-label">Compression Ratio</div>
                    <div class="metric-value">${data.compression_ratio}</div>
                </div>
                ${data.actual_ratio ? `
                <div class="metric-item" style="background: #fff3cd;">
                    <div class="metric-label">⬇️ Download Ratio</div>
                    <div class="metric-value" style="color: #856404; font-weight: bold;">${data.actual_ratio}</div>
                </div>
                ` : ''}
                <div class="metric-item">
                    <div class="metric-label">Space Savings</div>
                    <div class="metric-value">${data.space_savings}%</div>
                </div>
                ${data.actual_savings ? `
                <div class="metric-item" style="background: #fff3cd;">
                    <div class="metric-label">⬇️ Download Savings</div>
                    <div class="metric-value" style="color: #856404; font-weight: bold;">${data.actual_savings}%</div>
                </div>
                ` : ''}
                <div class="metric-item">
                    <div class="metric-label">Compression Time</div>
                    <div class="metric-value">${data.compression_time}s</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">Decompression Time</div>
                    <div class="metric-value">${data.decompression_time}s</div>
                </div>
            </div>
            ${data.actual_ratio > 1 ? `
            <div style="margin-top: 20px; padding: 15px; background: #ffebee; border-radius: 8px; border-left: 4px solid #f44336;">
                <p style="margin: 0 0 10px 0; color: #c62828; font-size: 0.95em;">
                    <strong>⚠️ File Expanded (${data.actual_ratio}x larger)!</strong>
                </p>
                <p style="margin: 0; color: #c62828; font-size: 0.9em;">
                    <strong>Solution:</strong> Use the <strong>resize option (50% or 25%)</strong> above to dramatically reduce file sizes!
                </p>
            </div>
            ` : data.actual_ratio > 0.8 ? `
            <div style="margin-top: 20px; padding: 15px; background: #fff3cd; border-radius: 8px; border-left: 4px solid #ffc107;">
                <p style="margin: 0; color: #856404; font-size: 0.9em;">
                    <strong>💡 Tip:</strong> Try the <strong>resize option (50%)</strong> for better compression!
                </p>
            </div>
            ` : `
            <div style="margin-top: 20px; padding: 15px; background: #e8f5e9; border-radius: 8px; border-left: 4px solid #4caf50;">
                <p style="margin: 0; color: #2e7d32; font-size: 0.9em;">
                    <strong>✓ Good compression!</strong> The file is ${data.actual_savings}% smaller.
                </p>
            </div>
            `}
            <div style="margin-top: 15px; text-align: center;">
                <span class="${data.is_correct ? 'success' : 'error'}">
                    ${data.is_correct ? '✓ Data integrity verified' : '✗ Data integrity check failed'}
                </span>
            </div>
        </div>
    `;
}

function displayComparison(results) {
    const resultsContent = document.getElementById('resultsContent');
    
    let html = '<h4 style="color: var(--primary-color); margin-bottom: 20px;">Algorithm Comparison</h4>';
    
    // Find best performers
    let bestRatio = null;
    let fastestCompression = null;
    
    results.forEach(data => {
        if (!data.error) {
            if (!bestRatio || data.compression_ratio < bestRatio.compression_ratio) {
                bestRatio = data;
            }
            if (!fastestCompression || data.compression_time < fastestCompression.compression_time) {
                fastestCompression = data;
            }
        }
    });
    
    results.forEach(data => {
        if (data.error) {
            html += `
                <div class="result-card">
                    <div class="result-header">${data.algorithm} - Error</div>
                    <div class="error">${data.error}</div>
                </div>
            `;
        } else {
            const isBestRatio = bestRatio && data.algorithm === bestRatio.algorithm;
            const isFastest = fastestCompression && data.algorithm === fastestCompression.algorithm;
            const badges = [];
            if (isBestRatio) badges.push('🏆 Best Ratio');
            if (isFastest) badges.push('⚡ Fastest');
            
            let downloadButtons = '';
            if (data.record_id && data.original_file_id && data.compressed_file_id) {
                downloadButtons = `
                    <div style="display: flex; gap: 10px; justify-content: center; margin-top: 15px; flex-wrap: wrap;">
                        <button onclick="downloadFile('original', '${data.original_file_id}')" 
                                style="padding: 8px 16px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; border-radius: 6px; cursor: pointer; font-size: 13px;">
                            📥 Original
                        </button>
                        <button onclick="downloadFile('compressed', '${data.compressed_file_id}')" 
                                style="padding: 8px 16px; background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; border: none; border-radius: 6px; cursor: pointer; font-size: 13px;">
                            📦 Compressed (.pkl)
                        </button>
                        <button onclick="downloadCompressedDat('${data.compressed_file_id}')" 
                                style="padding: 8px 16px; background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); color: white; border: none; border-radius: 6px; cursor: pointer; font-size: 13px;">
                            💾 Compressed (.dat)
                        </button>
                        <button onclick="generateReport('${data.record_id}')" 
                                style="padding: 8px 16px; background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); color: white; border: none; border-radius: 6px; cursor: pointer; font-size: 13px;">
                            📄 Report
                        </button>
                    </div>
                `;
            }
            
            html += `
                <div class="result-card">
                    <div class="result-header">
                        ${data.algorithm}
                        ${badges.length > 0 ? '<span style="color: #f5576c; margin-left: 10px;">' + badges.join(' ') + '</span>' : ''}
                    </div>
                    ${data.record_id ? `<div style="text-align: center; color: var(--primary-color); margin: 5px 0; font-size: 12px;">ID: ${data.record_id}</div>` : ''}
                    <div class="metrics-grid">
                        <div class="metric-item">
                            <div class="metric-label">Compression Ratio</div>
                            <div class="metric-value">${data.compression_ratio}</div>
                        </div>
                        <div class="metric-item">
                            <div class="metric-label">Space Savings</div>
                            <div class="metric-value">${data.space_savings}%</div>
                        </div>
                        <div class="metric-item">
                            <div class="metric-label">Compression Time</div>
                            <div class="metric-value">${data.compression_time}s</div>
                        </div>
                        <div class="metric-item">
                            <div class="metric-label">Status</div>
                            <div class="metric-value ${data.is_correct ? 'success' : 'error'}">
                                ${data.is_correct ? '✓' : '✗'}
                            </div>
                        </div>
                    </div>
                    ${downloadButtons}
                </div>
            `;
        }
    });
    
    resultsContent.innerHTML = html;
}

function downloadFile(type, fileId) {
    window.location.href = `/download/${type}/${fileId}`;
}

function downloadCompressedDat(fileId) {
    window.location.href = `/download/compressed/dat/${fileId}`;
}

function generateReport(recordId) {
    window.location.href = `/report/single/${recordId}`;
}

function toggleDarkMode() {
    document.body.classList.toggle('dark-mode');
    const isDark = document.body.classList.contains('dark-mode');
    localStorage.setItem('darkMode', isDark);
    document.querySelector('.dark-mode-toggle').textContent = isDark ? '☀️' : '🌙';
}

// Load saved dark mode preference
if(localStorage.getItem('darkMode') === 'true') {
    document.body.classList.add('dark-mode');
    document.querySelector('.dark-mode-toggle').textContent = '☀️';
}
</script>
"""

# Video compression page
VIDEO_PAGE = COMMON_CSS + """
<button class="dark-mode-toggle" onclick="toggleDarkMode()" title="Toggle Dark Mode">🌙</button>

<div class="container">
    <div class="header">
        <h1>🎥 Video Compression</h1>
        <p>Upload a video and compress it with different algorithms</p>
    </div>
    
    <div class="nav-bar">
        <a href="/" class="nav-button">🏠 Home</a>
        <a href="/text" class="nav-button">📝 Text</a>
        <a href="/images" class="nav-button">🖼️ Images</a>
        <a href="/videos" class="nav-button active">🎥 Videos</a>
        <a href="/documents" class="nav-button">📄 Documents</a>
        <a href="/decompress" class="nav-button">🔓 Decompress</a>
        <a href="/history" class="nav-button">📊 History</a>
    </div>
    
    <div class="content">
        <div class="section">
            <h3 class="section-title">Upload Video</h3>
            <div class="upload-area" id="uploadArea">
                <div class="upload-icon">📤</div>
                <h3>Click to upload or drag and drop</h3>
                <p>Supported formats: MP4, AVI, MOV</p>
                <input type="file" id="fileInput" accept=".mp4,.avi,.mov">
            </div>
            
            <div class="checkbox-container">
                <input type="checkbox" id="grayscale">
                <label for="grayscale">Convert to grayscale before compression</label>
            </div>
            
            <div id="fileInfo" style="margin-top: 20px; display: none;">
                <p><strong>Selected file:</strong> <span id="fileName"></span></p>
                <p><strong>File size:</strong> <span id="fileSize"></span></p>
            </div>
            
            <div class="algorithm-buttons">
                <button class="algo-button" onclick="compressVideo('rle')" id="rleBtn" disabled>
                    🔄 Compress with RLE
                </button>
                <button class="algo-button" onclick="compressVideo('huffman')" id="huffmanBtn" disabled>
                    🌳 Compress with Huffman
                </button>
                <button class="algo-button" onclick="compressVideo('lzw')" id="lzwBtn" disabled>
                    📚 Compress with LZW
                </button>
                <button class="algo-button" onclick="compressVideoAll()" id="allBtn" disabled>
                    ⚡ Compare All Algorithms
                </button>
            </div>
        </div>
        
        <div class="results-area" id="resultsArea">
            <h3 class="section-title">Compression Results</h3>
            <div id="resultsContent"></div>
        </div>
    </div>
</div>

<script>
let selectedFile = null;

const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const fileInfo = document.getElementById('fileInfo');
const fileName = document.getElementById('fileName');
const fileSize = document.getElementById('fileSize');
const buttons = ['rleBtn', 'huffmanBtn', 'lzwBtn', 'allBtn'];

// Click to upload
uploadArea.addEventListener('click', () => fileInput.click());

// File input change
fileInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        handleFile(e.target.files[0]);
    }
});

// Drag and drop functionality
uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    e.stopPropagation();
    uploadArea.style.borderColor = '#764ba2';
    uploadArea.style.background = '#f0f0ff';
});

uploadArea.addEventListener('dragleave', (e) => {
    e.preventDefault();
    e.stopPropagation();
    uploadArea.style.borderColor = '#667eea';
    uploadArea.style.background = 'white';
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    e.stopPropagation();
    uploadArea.style.borderColor = '#667eea';
    uploadArea.style.background = 'white';
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFile(files[0]);
    }
});

function handleFile(file) {
    selectedFile = file;
    fileName.textContent = selectedFile.name;
    fileSize.textContent = (selectedFile.size / 1024).toFixed(2) + ' KB';
    fileInfo.style.display = 'block';
    buttons.forEach(id => document.getElementById(id).disabled = false);
}

async function compressVideo(algorithm) {
    if (!selectedFile) return;
    
    const formData = new FormData();
    formData.append('file', selectedFile);
    formData.append('grayscale', document.getElementById('grayscale').checked);
    
    const resultsArea = document.getElementById('resultsArea');
    const resultsContent = document.getElementById('resultsContent');
    
    resultsArea.classList.add('show');
    resultsContent.innerHTML = '<div class="loading"></div> Compressing with ' + algorithm.toUpperCase() + '...';
    
    try {
        const response = await fetch(`/${algorithm}/compress/video`, {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (data.error) {
            resultsContent.innerHTML = `<div class="error">Error: ${data.error}</div>`;
        } else {
            displayResult(data);
        }
    } catch (error) {
        resultsContent.innerHTML = `<div class="error">Error: ${error.message}</div>`;
    }
}

async function compressVideoAll() {
    if (!selectedFile) return;
    
    const resultsArea = document.getElementById('resultsArea');
    const resultsContent = document.getElementById('resultsContent');
    
    resultsArea.classList.add('show');
    resultsContent.innerHTML = '<div class="loading"></div> Compressing with all algorithms...';
    
    const algorithms = ['rle', 'huffman', 'lzw'];
    const results = [];
    
    for (const algo of algorithms) {
        const formData = new FormData();
        formData.append('file', selectedFile);
        formData.append('grayscale', document.getElementById('grayscale').checked);
        
        try {
            const response = await fetch(`/${algo}/compress/video`, {
                method: 'POST',
                body: formData
            });
            const data = await response.json();
            results.push(data);
        } catch (error) {
            results.push({ algorithm: algo, error: error.message });
        }
    }
    
    displayComparison(results);
}

function displayResult(data) {
    const resultsContent = document.getElementById('resultsContent');
    
    resultsContent.innerHTML = `
        <div class="result-card">
            <div class="result-header">${data.algorithm} Compression Results</div>
            <div class="metrics-grid">
                <div class="metric-item">
                    <div class="metric-label">Original Size</div>
                    <div class="metric-value">${(data.original_size / 1024).toFixed(2)} KB</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">Compressed Size</div>
                    <div class="metric-value">${(data.compressed_size / 1024).toFixed(2)} KB</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">Compression Ratio</div>
                    <div class="metric-value">${data.compression_ratio}</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">Space Savings</div>
                    <div class="metric-value">${data.space_savings}%</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">Compression Time</div>
                    <div class="metric-value">${data.compression_time}s</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">Decompression Time</div>
                    <div class="metric-value">${data.decompression_time}s</div>
                </div>
            </div>
            <div style="margin-top: 20px; text-align: center;">
                <span class="${data.is_correct ? 'success' : 'error'}">
                    ${data.is_correct ? '✓ Data integrity verified' : '✗ Data integrity check failed'}
                </span>
            </div>
        </div>
    `;
}

function displayComparison(results) {
    const resultsContent = document.getElementById('resultsContent');
    
    let html = '<h4 style="color: var(--primary-color); margin-bottom: 20px;">Algorithm Comparison</h4>';
    
    // Find best performers
    let bestRatio = null;
    let fastestCompression = null;
    
    results.forEach(data => {
        if (!data.error) {
            if (!bestRatio || data.compression_ratio < bestRatio.compression_ratio) {
                bestRatio = data;
            }
            if (!fastestCompression || data.compression_time < fastestCompression.compression_time) {
                fastestCompression = data;
            }
        }
    });
    
    results.forEach(data => {
        if (data.error) {
            html += `
                <div class="result-card">
                    <div class="result-header">${data.algorithm} - Error</div>
                    <div class="error">${data.error}</div>
                </div>
            `;
        } else {
            const isBestRatio = bestRatio && data.algorithm === bestRatio.algorithm;
            const isFastest = fastestCompression && data.algorithm === fastestCompression.algorithm;
            const badges = [];
            if (isBestRatio) badges.push('🏆 Best Ratio');
            if (isFastest) badges.push('⚡ Fastest');
            
            let downloadButtons = '';
            if (data.record_id && data.original_file_id && data.compressed_file_id) {
                downloadButtons = `
                    <div style="display: flex; gap: 10px; justify-content: center; margin-top: 15px; flex-wrap: wrap;">
                        <button onclick="downloadFile('original', '${data.original_file_id}')" 
                                style="padding: 8px 16px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; border-radius: 6px; cursor: pointer; font-size: 13px;">
                            📥 Original
                        </button>
                        <button onclick="downloadFile('compressed', '${data.compressed_file_id}')" 
                                style="padding: 8px 16px; background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; border: none; border-radius: 6px; cursor: pointer; font-size: 13px;">
                            📦 Compressed (.pkl)
                        </button>
                        <button onclick="downloadCompressedDat('${data.compressed_file_id}')" 
                                style="padding: 8px 16px; background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); color: white; border: none; border-radius: 6px; cursor: pointer; font-size: 13px;">
                            💾 Compressed (.dat)
                        </button>
                        <button onclick="generateReport('${data.record_id}')" 
                                style="padding: 8px 16px; background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); color: white; border: none; border-radius: 6px; cursor: pointer; font-size: 13px;">
                            📄 Report
                        </button>
                    </div>
                `;
            }
            
            html += `
                <div class="result-card">
                    <div class="result-header">
                        ${data.algorithm}
                        ${badges.length > 0 ? '<span style="color: #f5576c; margin-left: 10px;">' + badges.join(' ') + '</span>' : ''}
                    </div>
                    ${data.record_id ? `<div style="text-align: center; color: var(--primary-color); margin: 5px 0; font-size: 12px;">ID: ${data.record_id}</div>` : ''}
                    <div class="metrics-grid">
                        <div class="metric-item">
                            <div class="metric-label">Compression Ratio</div>
                            <div class="metric-value">${data.compression_ratio}</div>
                        </div>
                        <div class="metric-item">
                            <div class="metric-label">Space Savings</div>
                            <div class="metric-value">${data.space_savings}%</div>
                        </div>
                        <div class="metric-item">
                            <div class="metric-label">Compression Time</div>
                            <div class="metric-value">${data.compression_time}s</div>
                        </div>
                        <div class="metric-item">
                            <div class="metric-label">Status</div>
                            <div class="metric-value ${data.is_correct ? 'success' : 'error'}">
                                ${data.is_correct ? '✓' : '✗'}
                            </div>
                        </div>
                    </div>
                    ${downloadButtons}
                </div>
            `;
        }
    });
    
    resultsContent.innerHTML = html;
}

function downloadFile(type, fileId) {
    window.location.href = `/download/${type}/${fileId}`;
}

function downloadCompressedDat(fileId) {
    window.location.href = `/download/compressed/dat/${fileId}`;
}

function generateReport(recordId) {
    window.location.href = `/report/single/${recordId}`;
}

function toggleDarkMode() {
    document.body.classList.toggle('dark-mode');
    const isDark = document.body.classList.contains('dark-mode');
    localStorage.setItem('darkMode', isDark);
    document.querySelector('.dark-mode-toggle').textContent = isDark ? '☀️' : '🌙';
}

// Load saved dark mode preference
if(localStorage.getItem('darkMode') === 'true') {
    document.body.classList.add('dark-mode');
    document.querySelector('.dark-mode-toggle').textContent = '☀️';
}
</script>
"""

# Document compression page
DOCUMENT_PAGE = COMMON_CSS + """
<button class="dark-mode-toggle" onclick="toggleDarkMode()" title="Toggle Dark Mode">🌙</button>

<div class="container">
    <div class="header">
        <h1>📄 Document Compression</h1>
        <p>Upload a document and compress it with different algorithms</p>
    </div>
    
    <div class="nav-bar">
        <a href="/" class="nav-button">🏠 Home</a>
        <a href="/text" class="nav-button">📝 Text</a>
        <a href="/images" class="nav-button">🖼️ Images</a>
        <a href="/videos" class="nav-button">🎥 Videos</a>
        <a href="/documents" class="nav-button active">📄 Documents</a>
        <a href="/decompress" class="nav-button">🔓 Decompress</a>
        <a href="/history" class="nav-button">📊 History</a>
    </div>
    
    <div class="content">
        <div class="section">
            <h3 class="section-title">Upload Document</h3>
            <div class="upload-area" id="uploadArea">
                <div class="upload-icon">📤</div>
                <h3>Click to upload or drag and drop</h3>
                <p>Supported formats: TXT, PDF, DOCX, CSV</p>
                <input type="file" id="fileInput" accept=".txt,.pdf,.docx,.csv">
            </div>
            
            <div id="fileInfo" style="margin-top: 20px; display: none;">
                <p><strong>Selected file:</strong> <span id="fileName"></span></p>
                <p><strong>File size:</strong> <span id="fileSize"></span></p>
            </div>
            
            <div class="algorithm-buttons">
                <button class="algo-button" onclick="compressDocument('rle')" id="rleBtn" disabled>
                    🔄 Compress with RLE
                </button>
                <button class="algo-button" onclick="compressDocument('huffman')" id="huffmanBtn" disabled>
                    🌳 Compress with Huffman
                </button>
                <button class="algo-button" onclick="compressDocument('lzw')" id="lzwBtn" disabled>
                    📚 Compress with LZW
                </button>
                <button class="algo-button" onclick="compressDocumentAll()" id="allBtn" disabled>
                    ⚡ Compare All Algorithms
                </button>
            </div>
        </div>
        
        <div class="results-area" id="resultsArea">
            <h3 class="section-title">Compression Results</h3>
            <div id="resultsContent"></div>
        </div>
    </div>
</div>

<script>
let selectedFile = null;

const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const fileInfo = document.getElementById('fileInfo');
const fileName = document.getElementById('fileName');
const fileSize = document.getElementById('fileSize');
const buttons = ['rleBtn', 'huffmanBtn', 'lzwBtn', 'allBtn'];

// Click to upload
uploadArea.addEventListener('click', () => fileInput.click());

// File input change
fileInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        handleFile(e.target.files[0]);
    }
});

// Drag and drop functionality
uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    e.stopPropagation();
    const primaryColor = getComputedStyle(document.documentElement).getPropertyValue('--secondary-color').trim();
    uploadArea.style.borderColor = primaryColor;
    uploadArea.style.background = 'rgba(102, 126, 234, 0.1)';
});

uploadArea.addEventListener('dragleave', (e) => {
    e.preventDefault();
    e.stopPropagation();
    const primaryColor = getComputedStyle(document.documentElement).getPropertyValue('--primary-color').trim();
    uploadArea.style.borderColor = primaryColor;
    uploadArea.style.background = '';
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    e.stopPropagation();
    const primaryColor = getComputedStyle(document.documentElement).getPropertyValue('--primary-color').trim();
    uploadArea.style.borderColor = primaryColor;
    uploadArea.style.background = '';
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFile(files[0]);
    }
});

function handleFile(file) {
    selectedFile = file;
    fileName.textContent = selectedFile.name;
    fileSize.textContent = (selectedFile.size / 1024).toFixed(2) + ' KB';
    fileInfo.style.display = 'block';
    buttons.forEach(id => document.getElementById(id).disabled = false);
}

async function compressDocument(algorithm) {
    if (!selectedFile) return;
    
    const formData = new FormData();
    formData.append('file', selectedFile);
    
    const resultsArea = document.getElementById('resultsArea');
    const resultsContent = document.getElementById('resultsContent');
    
    resultsArea.classList.add('show');
    resultsContent.innerHTML = '<div class="loading"></div> Compressing with ' + algorithm.toUpperCase() + '...';
    
    try {
        const response = await fetch(`/${algorithm}/compress/document`, {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (data.error) {
            resultsContent.innerHTML = `<div class="error">Error: ${data.error}</div>`;
        } else {
            displayResult(data);
        }
    } catch (error) {
        resultsContent.innerHTML = `<div class="error">Error: ${error.message}</div>`;
    }
}

async function compressDocumentAll() {
    if (!selectedFile) return;
    
    const resultsArea = document.getElementById('resultsArea');
    const resultsContent = document.getElementById('resultsContent');
    
    resultsArea.classList.add('show');
    resultsContent.innerHTML = '<div class="loading"></div> Compressing with all algorithms...';
    
    const algorithms = ['rle', 'huffman', 'lzw'];
    const results = [];
    
    for (const algo of algorithms) {
        const formData = new FormData();
        formData.append('file', selectedFile);
        
        try {
            const response = await fetch(`/${algo}/compress/document`, {
                method: 'POST',
                body: formData
            });
            const data = await response.json();
            results.push(data);
        } catch (error) {
            results.push({ algorithm: algo, error: error.message });
        }
    }
    
    displayComparison(results);
}

function displayResult(data) {
    const resultsContent = document.getElementById('resultsContent');
    
    let downloadButtons = '';
    if (data.record_id && data.original_file_id && data.compressed_file_id) {
        downloadButtons = `
            <div style="display: flex; gap: 15px; justify-content: center; margin-top: 20px; flex-wrap: wrap;">
                <button onclick="downloadFile('original', '${data.original_file_id}')" 
                        style="padding: 12px 24px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; border-radius: 8px; cursor: pointer; font-size: 16px; transition: all 0.3s;">
                    📥 Download Original
                </button>
                <button onclick="downloadFile('compressed', '${data.compressed_file_id}')" 
                        style="padding: 12px 24px; background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; border: none; border-radius: 8px; cursor: pointer; font-size: 16px; transition: all 0.3s;">
                    📦 Download Compressed (.pkl)
                </button>
                <button onclick="downloadCompressedDat('${data.compressed_file_id}')" 
                        style="padding: 12px 24px; background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); color: white; border: none; border-radius: 8px; cursor: pointer; font-size: 16px; transition: all 0.3s;">
                    💾 Download Compressed (.dat)
                </button>
                <button onclick="generateReport('${data.record_id}')" 
                        style="padding: 12px 24px; background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); color: white; border: none; border-radius: 8px; cursor: pointer; font-size: 16px; transition: all 0.3s;">
                    📄 Generate Report
                </button>
            </div>
        `;
    }
    
    resultsContent.innerHTML = `
        <div class="result-card">
            <div class="result-header">${data.algorithm} Compression Results</div>
            ${data.record_id ? `<div style="text-align: center; color: #667eea; margin: 10px 0; font-size: 14px;">Record ID: ${data.record_id}</div>` : ''}
            <div class="metrics-grid">
                <div class="metric-item">
                    <div class="metric-label">Original Size</div>
                    <div class="metric-value">${(data.original_size / 1024).toFixed(2)} KB</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">Compressed Size</div>
                    <div class="metric-value">${(data.compressed_size / 1024).toFixed(2)} KB</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">Compression Ratio</div>
                    <div class="metric-value">${data.compression_ratio}</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">Space Savings</div>
                    <div class="metric-value">${data.space_savings}%</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">Compression Time</div>
                    <div class="metric-value">${data.compression_time}s</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">Decompression Time</div>
                    <div class="metric-value">${data.decompression_time}s</div>
                </div>
            </div>
            <div style="margin-top: 20px; text-align: center;">
                <span class="${data.is_correct ? 'success' : 'error'}">
                    ${data.is_correct ? '✓ Data integrity verified' : '✗ Data integrity check failed'}
                </span>
            </div>
        </div>
    `;
}

function displayComparison(results) {
    const resultsContent = document.getElementById('resultsContent');
    
    let html = '<h4 style="color: #667eea; margin-bottom: 20px;">Algorithm Comparison</h4>';
    
    // Find best performers
    let bestRatio = null;
    let fastestCompression = null;
    
    results.forEach(data => {
        if (!data.error) {
            if (!bestRatio || data.compression_ratio < bestRatio.compression_ratio) {
                bestRatio = data;
            }
            if (!fastestCompression || data.compression_time < fastestCompression.compression_time) {
                fastestCompression = data;
            }
        }
    });
    
    results.forEach(data => {
        if (data.error) {
            html += `
                <div class="result-card">
                    <div class="result-header">${data.algorithm} - Error</div>
                    <div class="error">${data.error}</div>
                </div>
            `;
        } else {
            const isBestRatio = bestRatio && data.algorithm === bestRatio.algorithm;
            const isFastest = fastestCompression && data.algorithm === fastestCompression.algorithm;
            const badges = [];
            if (isBestRatio) badges.push('🏆 Best Ratio');
            if (isFastest) badges.push('⚡ Fastest');
            
            let downloadButtons = '';
            if (data.record_id && data.original_file_id && data.compressed_file_id) {
                downloadButtons = `
                    <div style="display: flex; gap: 10px; justify-content: center; margin-top: 15px; flex-wrap: wrap;">
                        <button onclick="downloadFile('original', '${data.original_file_id}')" 
                                style="padding: 8px 16px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; border-radius: 6px; cursor: pointer; font-size: 13px;">
                            📥 Original
                        </button>
                        <button onclick="downloadFile('compressed', '${data.compressed_file_id}')" 
                                style="padding: 8px 16px; background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; border: none; border-radius: 6px; cursor: pointer; font-size: 13px;">
                            📦 Compressed (.pkl)
                        </button>
                        <button onclick="downloadCompressedDat('${data.compressed_file_id}')" 
                                style="padding: 8px 16px; background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); color: white; border: none; border-radius: 6px; cursor: pointer; font-size: 13px;">
                            💾 Compressed (.dat)
                        </button>
                        <button onclick="generateReport('${data.record_id}')" 
                                style="padding: 8px 16px; background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); color: white; border: none; border-radius: 6px; cursor: pointer; font-size: 13px;">
                            📄 Report
                        </button>
                    </div>
                `;
            }
            
            html += `
                <div class="result-card">
                    <div class="result-header">
                        ${data.algorithm}
                        ${badges.length > 0 ? '<span style="color: #f5576c; margin-left: 10px;">' + badges.join(' ') + '</span>' : ''}
                    </div>
                    ${data.record_id ? `<div style="text-align: center; color: var(--primary-color); margin: 5px 0; font-size: 12px;">ID: ${data.record_id}</div>` : ''}
                    <div class="metrics-grid">
                        <div class="metric-item">
                            <div class="metric-label">Compression Ratio</div>
                            <div class="metric-value">${data.compression_ratio}</div>
                        </div>
                        <div class="metric-item">
                            <div class="metric-label">Space Savings</div>
                            <div class="metric-value">${data.space_savings}%</div>
                        </div>
                        <div class="metric-item">
                            <div class="metric-label">Compression Time</div>
                            <div class="metric-value">${data.compression_time}s</div>
                        </div>
                        <div class="metric-item">
                            <div class="metric-label">Status</div>
                            <div class="metric-value ${data.is_correct ? 'success' : 'error'}">
                                ${data.is_correct ? '✓' : '✗'}
                            </div>
                        </div>
                    </div>
                    ${downloadButtons}
                </div>
            `;
        }
    });
    
    resultsContent.innerHTML = html;
}

function downloadFile(type, fileId) {
    window.location.href = `/download/${type}/${fileId}`;
}

function downloadCompressedDat(fileId) {
    window.location.href = `/download/compressed/dat/${fileId}`;
}

function generateReport(recordId) {
    window.location.href = `/report/single/${recordId}`;
}

function toggleDarkMode() {
    document.body.classList.toggle('dark-mode');
    const isDark = document.body.classList.contains('dark-mode');
    localStorage.setItem('darkMode', isDark);
    document.querySelector('.dark-mode-toggle').textContent = isDark ? '☀️' : '🌙';
}

// Load saved dark mode preference
if(localStorage.getItem('darkMode') === 'true') {
    document.body.classList.add('dark-mode');
    document.querySelector('.dark-mode-toggle').textContent = '☀️';
}
</script>
"""

# Text compression page
TEXT_PAGE = COMMON_CSS + """
<style>
    textarea {
        width: 100%;
        padding: 15px;
        border: 2px solid var(--border-color);
        border-radius: 8px;
        font-family: 'Courier New', monospace;
        font-size: 14px;
        resize: vertical;
        transition: border-color 0.3s;
        min-height: 200px;
        background: var(--container-bg);
        color: var(--text-color);
    }
    
    textarea:focus {
        outline: none;
        border-color: var(--primary-color);
    }
</style>
<button class="dark-mode-toggle" onclick="toggleDarkMode()" title="Toggle Dark Mode">🌙</button>

<div class="container">
    <div class="header">
        <h1>📝 Text Compression</h1>
        <p>Enter text and compare compression algorithms</p>
    </div>
    
    <div class="nav-bar">
        <a href="/" class="nav-button">🏠 Home</a>
        <a href="/text" class="nav-button active">📝 Text</a>
        <a href="/images" class="nav-button">🖼️ Images</a>
        <a href="/videos" class="nav-button">🎥 Videos</a>
        <a href="/documents" class="nav-button">📄 Documents</a>
        <a href="/decompress" class="nav-button">🔓 Decompress</a>
        <a href="/history" class="nav-button">📊 History</a>
    </div>
    
    <div class="content">
        <div class="section">
            <h3 class="section-title">Enter Your Text</h3>
            <textarea id="textInput" placeholder="Type or paste your text here... (e.g., 'Hello World! Hello World! Hello World!')"></textarea>
            
            <div style="margin-top: 15px; color: #666;">
                <span id="charCount">0</span> characters
            </div>
            
            <div class="algorithm-buttons">
                <button class="algo-button" onclick="compressText('rle')" id="rleBtn">
                    🔄 Compress with RLE
                </button>
                <button class="algo-button" onclick="compressText('huffman')" id="huffmanBtn">
                    🌳 Compress with Huffman
                </button>
                <button class="algo-button" onclick="compressText('lzw')" id="lzwBtn">
                    📚 Compress with LZW
                </button>
                <button class="algo-button" onclick="compressTextAll()" id="allBtn">
                    ⚡ Compare All Algorithms
                </button>
            </div>
        </div>
        
        <div class="results-area" id="resultsArea">
            <h3 class="section-title">Compression Results</h3>
            <div id="resultsContent"></div>
        </div>
    </div>
</div>

<script>
const textInput = document.getElementById('textInput');
const charCount = document.getElementById('charCount');

textInput.addEventListener('input', () => {
    charCount.textContent = textInput.value.length;
});

async function compressText(algorithm) {
    const text = textInput.value;
    
    if (!text) {
        alert('Please enter some text to compress');
        return;
    }
    
    const resultsArea = document.getElementById('resultsArea');
    const resultsContent = document.getElementById('resultsContent');
    
    resultsArea.classList.add('show');
    resultsContent.innerHTML = '<div class="loading"></div> Compressing with ' + algorithm.toUpperCase() + '...';
    
    try {
        const response = await fetch(`/${algorithm}/compress/text`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text: text })
        });
        
        const data = await response.json();
        
        if (data.error) {
            resultsContent.innerHTML = `<div class="error">Error: ${data.error}</div>`;
        } else {
            displayResult(data);
        }
    } catch (error) {
        resultsContent.innerHTML = `<div class="error">Error: ${error.message}</div>`;
    }
}

async function compressTextAll() {
    const text = textInput.value;
    
    if (!text) {
        alert('Please enter some text to compress');
        return;
    }
    
    const resultsArea = document.getElementById('resultsArea');
    const resultsContent = document.getElementById('resultsContent');
    
    resultsArea.classList.add('show');
    resultsContent.innerHTML = '<div class="loading"></div> Compressing with all algorithms...';
    
    const algorithms = ['rle', 'huffman', 'lzw'];
    const results = [];
    
    for (const algo of algorithms) {
        try {
            const response = await fetch(`/${algo}/compress/text`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ text: text })
            });
            const data = await response.json();
            results.push(data);
        } catch (error) {
            results.push({ algorithm: algo, error: error.message });
        }
    }
    
    displayComparison(results);
}

function displayResult(data) {
    const resultsContent = document.getElementById('resultsContent');
    
    let downloadButtons = '';
    if (data.record_id && data.original_file_id && data.compressed_file_id) {
        downloadButtons = `
            <div style="display: flex; gap: 15px; justify-content: center; margin-top: 20px; flex-wrap: wrap;">
                <button onclick="downloadFile('original', '${data.original_file_id}')" 
                        style="padding: 12px 24px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; border-radius: 8px; cursor: pointer; font-size: 16px; transition: all 0.3s;">
                    📥 Download Original
                </button>
                <button onclick="downloadFile('compressed', '${data.compressed_file_id}')" 
                        style="padding: 12px 24px; background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; border: none; border-radius: 8px; cursor: pointer; font-size: 16px; transition: all 0.3s;">
                    📦 Download Compressed (.pkl)
                </button>
                <button onclick="downloadCompressedDat('${data.compressed_file_id}')" 
                        style="padding: 12px 24px; background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); color: white; border: none; border-radius: 8px; cursor: pointer; font-size: 16px; transition: all 0.3s;">
                    💾 Download Compressed (.dat)
                </button>
                <button onclick="generateReport('${data.record_id}')" 
                        style="padding: 12px 24px; background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); color: white; border: none; border-radius: 8px; cursor: pointer; font-size: 16px; transition: all 0.3s;">
                    📄 Generate Report
                </button>
            </div>
        `;
    }
    
    resultsContent.innerHTML = `
        <div class="result-card">
            <div class="result-header">${data.algorithm} Compression Results</div>
            ${data.record_id ? `<div style="text-align: center; color: #667eea; margin: 10px 0; font-size: 14px;">Record ID: ${data.record_id}</div>` : ''}
            <div class="metrics-grid">
                <div class="metric-item">
                    <div class="metric-label">Original Size</div>
                    <div class="metric-value">${data.original_size} bytes</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">Compressed Size</div>
                    <div class="metric-value">${data.compressed_size} bytes</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">Compression Ratio</div>
                    <div class="metric-value">${data.compression_ratio}</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">Space Savings</div>
                    <div class="metric-value">${data.space_savings}%</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">Compression Time</div>
                    <div class="metric-value">${data.compression_time}s</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">Decompression Time</div>
                    <div class="metric-value">${data.decompression_time}s</div>
                </div>
            </div>
            <div style="margin-top: 20px; text-align: center;">
                <span class="${data.is_correct ? 'success' : 'error'}">
                    ${data.is_correct ? '✓ Data integrity verified' : '✗ Data integrity check failed'}
                </span>
            </div>
            ${downloadButtons}
        </div>
    `;
}

function downloadFile(type, fileId) {
    window.location.href = `/download/${type}/${fileId}`;
}

function generateReport(recordId) {
    window.location.href = `/report/single/${recordId}`;
}

function displayComparison(results) {
    const resultsContent = document.getElementById('resultsContent');
    
    let html = '<h4 style="color: #667eea; margin-bottom: 20px;">Algorithm Comparison</h4>';
    
    // Find best performers
    let bestRatio = null;
    let fastestCompression = null;
    
    results.forEach(data => {
        if (!data.error) {
            if (!bestRatio || data.compression_ratio < bestRatio.compression_ratio) {
                bestRatio = data;
            }
            if (!fastestCompression || data.compression_time < fastestCompression.compression_time) {
                fastestCompression = data;
            }
        }
    });
    
    results.forEach(data => {
        if (data.error) {
            html += `
                <div class="result-card">
                    <div class="result-header">${data.algorithm} - Error</div>
                    <div class="error">${data.error}</div>
                </div>
            `;
        } else {
            const isBestRatio = bestRatio && data.algorithm === bestRatio.algorithm;
            const isFastest = fastestCompression && data.algorithm === fastestCompression.algorithm;
            const badges = [];
            if (isBestRatio) badges.push('🏆 Best Ratio');
            if (isFastest) badges.push('⚡ Fastest');
            
            let downloadButtons = '';
            if (data.record_id && data.original_file_id && data.compressed_file_id) {
                downloadButtons = `
                    <div style="display: flex; gap: 10px; justify-content: center; margin-top: 15px; flex-wrap: wrap;">
                        <button onclick="downloadFile('original', '${data.original_file_id}')" 
                                style="padding: 8px 16px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; border-radius: 6px; cursor: pointer; font-size: 13px; transition: all 0.3s;">
                            📥 Original
                        </button>
                        <button onclick="downloadFile('compressed', '${data.compressed_file_id}')" 
                                style="padding: 8px 16px; background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; border: none; border-radius: 6px; cursor: pointer; font-size: 13px; transition: all 0.3s;">
                            📦 Compressed
                        </button>
                        <button onclick="generateReport('${data.record_id}')" 
                                style="padding: 8px 16px; background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); color: white; border: none; border-radius: 6px; cursor: pointer; font-size: 13px; transition: all 0.3s;">
                            📄 Report
                        </button>
                    </div>
                `;
            }
            
            html += `
                <div class="result-card">
                    <div class="result-header">
                        ${data.algorithm}
                        ${badges.length > 0 ? '<span style="color: #f5576c; margin-left: 10px;">' + badges.join(' ') + '</span>' : ''}
                    </div>
                    ${data.record_id ? `<div style="text-align: center; color: var(--primary-color); margin: 5px 0; font-size: 12px;">ID: ${data.record_id}</div>` : ''}
                    <div class="metrics-grid">
                        <div class="metric-item">
                            <div class="metric-label">Original Size</div>
                            <div class="metric-value">${data.original_size} bytes</div>
                        </div>
                        <div class="metric-item">
                            <div class="metric-label">Compressed Size</div>
                            <div class="metric-value">${data.compressed_size} bytes</div>
                        </div>
                        <div class="metric-item">
                            <div class="metric-label">Compression Ratio</div>
                            <div class="metric-value">${data.compression_ratio}</div>
                        </div>
                        <div class="metric-item">
                            <div class="metric-label">Space Savings</div>
                            <div class="metric-value">${data.space_savings}%</div>
                        </div>
                        <div class="metric-item">
                            <div class="metric-label">Compression Time</div>
                            <div class="metric-value">${data.compression_time}s</div>
                        </div>
                        <div class="metric-item">
                            <div class="metric-label">Status</div>
                            <div class="metric-value ${data.is_correct ? 'success' : 'error'}">
                                ${data.is_correct ? '✓' : '✗'}
                            </div>
                        </div>
                    </div>
                    ${downloadButtons}
                </div>
            `;
        }
    });
    
    resultsContent.innerHTML = html;
}

function toggleDarkMode() {
    document.body.classList.toggle('dark-mode');
    const isDark = document.body.classList.contains('dark-mode');
    localStorage.setItem('darkMode', isDark);
    document.querySelector('.dark-mode-toggle').textContent = isDark ? '☀️' : '🌙';
}

// Load saved dark mode preference
if(localStorage.getItem('darkMode') === 'true') {
    document.body.classList.add('dark-mode');
    document.querySelector('.dark-mode-toggle').textContent = '☀️';
}
</script>
"""

# History page
HISTORY_PAGE = COMMON_CSS + """
<button class="dark-mode-toggle" onclick="toggleDarkMode()" title="Toggle Dark Mode">🌙</button>

<div class="container">
    <div class="header">
        <h1>📊 Compression History & Reports</h1>
        <p>View your compression history and generate reports</p>
    </div>
    
    <div class="nav-bar">
        <a href="/" class="nav-button">🏠 Home</a>
        <a href="/text" class="nav-button">📝 Text</a>
        <a href="/images" class="nav-button">🖼️ Images</a>
        <a href="/videos" class="nav-button">🎥 Videos</a>
        <a href="/documents" class="nav-button">📄 Documents</a>
        <a href="/decompress" class="nav-button">🔓 Decompress</a>
        <a href="/history" class="nav-button active">📊 History</a>
    </div>
    
    <div class="content">
        <div class="section">
            <h3 class="section-title">Overall Statistics</h3>
            <div class="metrics-grid" style="margin-top: 20px;">
                <div class="metric-item">
                    <div class="metric-label">Total Compressions</div>
                    <div class="metric-value">{{ stats.total_compressions }}</div>
                </div>
                {% for algo, count in stats.algorithm_stats.items() %}
                <div class="metric-item">
                    <div class="metric-label">{{ algo }}</div>
                    <div class="metric-value">{{ count }}</div>
                </div>
                {% endfor %}
            </div>
            
            <div style="margin-top: 30px; text-align: center;">
                <a href="/report/history" class="nav-button" style="text-decoration: none;">
                    📄 Download Full History Report (PDF)
                </a>
            </div>
        </div>
        
        <div class="section">
            <h3 class="section-title">Recent Compression History</h3>
            <div style="overflow-x: auto;">
                <table style="width: 100%; border-collapse: collapse; margin-top: 20px;">
                    <thead>
                        <tr style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;">
                            <th style="padding: 12px; text-align: left;">Date/Time</th>
                            <th style="padding: 12px; text-align: left;">File</th>
                            <th style="padding: 12px; text-align: left;">Type</th>
                            <th style="padding: 12px; text-align: left;">Algorithm</th>
                            <th style="padding: 12px; text-align: center;">Ratio</th>
                            <th style="padding: 12px; text-align: center;">Savings</th>
                            <th style="padding: 12px; text-align: center;">Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for record in history %}
                        <tr style="border-bottom: 1px solid #e0e0e0;">
                            <td style="padding: 12px;">{{ record.timestamp.strftime('%Y-%m-%d %H:%M') if record.timestamp else 'N/A' }}</td>
                            <td style="padding: 12px;">{{ record.filename }}</td>
                            <td style="padding: 12px;">{{ record.file_type }}</td>
                            <td style="padding: 12px;">{{ record.algorithm }}</td>
                            <td style="padding: 12px; text-align: center;">{{ "%.4f"|format(record.compression_ratio) }}</td>
                            <td style="padding: 12px; text-align: center;">{{ "%.2f"|format(record.space_savings) }}%</td>
                            <td style="padding: 12px; text-align: center;">
                                <button onclick="downloadOriginal('{{ record.original_file_id }}')" 
                                        class="algo-button" style="padding: 5px 10px; font-size: 12px; margin: 2px;">
                                    📥 Original
                                </button>
                                <button onclick="downloadCompressed('{{ record.compressed_file_id }}')" 
                                        class="algo-button" style="padding: 5px 10px; font-size: 12px; margin: 2px;">
                                    📦 Compressed (.pkl)
                                </button>
                                <button onclick="downloadCompressedDat('{{ record.compressed_file_id }}')" 
                                        class="algo-button" style="padding: 5px 10px; font-size: 12px; margin: 2px;">
                                    💾 Compressed (.dat)
                                </button>
                                <button onclick="generateReport('{{ record._id }}')" 
                                        class="algo-button" style="padding: 5px 10px; font-size: 12px; margin: 2px;">
                                    📄 Report
                                </button>
                            </td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</div>

<script>
function downloadOriginal(fileId) {
    window.location.href = `/download/original/${fileId}`;
}

function downloadCompressed(fileId) {
    window.location.href = `/download/compressed/${fileId}`;
}

function downloadCompressedDat(fileId) {
    window.location.href = `/download/compressed/dat/${fileId}`;
}

function generateReport(recordId) {
    window.location.href = `/report/single/${recordId}`;
}

function toggleDarkMode() {
    document.body.classList.toggle('dark-mode');
    const isDark = document.body.classList.contains('dark-mode');
    localStorage.setItem('darkMode', isDark);
    document.querySelector('.dark-mode-toggle').textContent = isDark ? '☀️' : '🌙';
}

// Load saved dark mode preference
if(localStorage.getItem('darkMode') === 'true') {
    document.body.classList.add('dark-mode');
    document.querySelector('.dark-mode-toggle').textContent = '☀️';
}
</script>
"""

# Decompression page
DECOMPRESS_PAGE = COMMON_CSS + """
<button class="dark-mode-toggle" onclick="toggleDarkMode()" title="Toggle Dark Mode">🌙</button>

<div class="container">
    <div class="header">
        <h1>🔓 Decompress Files</h1>
        <p>Upload compressed files (.pkl or .dat) to decompress them</p>
    </div>
    
    <div class="nav-bar">
        <a href="/" class="nav-button">🏠 Home</a>
        <a href="/text" class="nav-button">📝 Text</a>
        <a href="/images" class="nav-button">🖼️ Images</a>
        <a href="/videos" class="nav-button">🎥 Videos</a>
        <a href="/documents" class="nav-button">📄 Documents</a>
        <a href="/decompress" class="nav-button active">🔓 Decompress</a>
        <a href="/history" class="nav-button">📊 History</a>
    </div>
    
    <div class="content">
        <!-- Instructions Banner -->
        <div class="section" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; margin-bottom: 20px; border-radius: 15px; box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);">
            <h3 style="margin: 0 0 15px 0; font-size: 1.3em;">💡 How to Decompress Files</h3>
            <div style="background: rgba(255, 255, 255, 0.15); padding: 15px; border-radius: 10px;">
                <p style="margin: 0 0 10px 0; font-size: 0.95em;"><strong>Step 1:</strong> Upload a compressed file (.pkl format)</p>
                <p style="margin: 0 0 10px 0; font-size: 0.95em;"><strong>Step 2:</strong> Select the algorithm used for compression</p>
                <p style="margin: 0; font-size: 0.95em;"><strong>Step 3:</strong> Click decompress and download your original file!</p>
            </div>
        </div>
        
        <div class="section">
            <h3 class="section-title">Upload Compressed File</h3>
            <div class="upload-area" id="uploadArea">
                <div class="upload-icon">📤</div>
                <h3>Click to upload or drag and drop</h3>
                <p>Supported formats: .pkl (compressed pickle files)</p>
                <input type="file" id="fileInput" accept=".pkl">
            </div>
            
            <div id="fileInfo" style="margin-top: 20px; display: none;">
                <p><strong>Selected file:</strong> <span id="fileName"></span></p>
                <p><strong>File size:</strong> <span id="fileSize"></span></p>
            </div>
            
            <div style="margin-top: 20px;">
                <label for="algorithmSelect" style="display: block; margin-bottom: 10px; font-weight: bold; color: var(--text-color);">
                    Select Compression Algorithm:
                </label>
                <select id="algorithmSelect" style="width: 100%; padding: 12px; border: 2px solid var(--border-color); border-radius: 8px; font-size: 16px; background: var(--container-bg); color: var(--text-color);">
                    <option value="">-- Choose Algorithm --</option>
                    <option value="rle">🔄 RLE (Run Length Encoding)</option>
                    <option value="huffman">🌳 Huffman Coding</option>
                    <option value="lzw">📚 LZW (Lempel-Ziv-Welch)</option>
                </select>
            </div>
            
            <div style="margin-top: 20px;">
                <button class="algo-button" onclick="decompressFile()" id="decompressBtn" disabled>
                    🔓 Decompress File
                </button>
            </div>
        </div>
        
        <div class="results-area" id="resultsArea">
            <h3 class="section-title">Decompression Results</h3>
            <div id="resultsContent"></div>
        </div>
    </div>
</div>

<script>
let selectedFile = null;

const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const fileInfo = document.getElementById('fileInfo');
const fileName = document.getElementById('fileName');
const fileSize = document.getElementById('fileSize');
const algorithmSelect = document.getElementById('algorithmSelect');
const decompressBtn = document.getElementById('decompressBtn');

// Click to upload
uploadArea.addEventListener('click', () => fileInput.click());

// File input change
fileInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        handleFile(e.target.files[0]);
    }
});

// Algorithm selection change
algorithmSelect.addEventListener('change', () => {
    updateDecompressButton();
});

// Drag and drop functionality
uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    e.stopPropagation();
    uploadArea.style.borderColor = '#764ba2';
    uploadArea.style.background = 'rgba(102, 126, 234, 0.1)';
});

uploadArea.addEventListener('dragleave', (e) => {
    e.preventDefault();
    e.stopPropagation();
    const primaryColor = getComputedStyle(document.documentElement).getPropertyValue('--primary-color').trim();
    uploadArea.style.borderColor = primaryColor;
    uploadArea.style.background = '';
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    e.stopPropagation();
    const primaryColor = getComputedStyle(document.documentElement).getPropertyValue('--primary-color').trim();
    uploadArea.style.borderColor = primaryColor;
    uploadArea.style.background = '';
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFile(files[0]);
    }
});

function handleFile(file) {
    selectedFile = file;
    fileName.textContent = selectedFile.name;
    fileSize.textContent = (selectedFile.size / 1024).toFixed(2) + ' KB';
    fileInfo.style.display = 'block';
    updateDecompressButton();
}

function updateDecompressButton() {
    decompressBtn.disabled = !(selectedFile && algorithmSelect.value);
}

async function decompressFile() {
    if (!selectedFile || !algorithmSelect.value) {
        alert('Please select a file and algorithm');
        return;
    }
    
    const formData = new FormData();
    formData.append('file', selectedFile);
    formData.append('algorithm', algorithmSelect.value);
    
    const resultsArea = document.getElementById('resultsArea');
    const resultsContent = document.getElementById('resultsContent');
    
    resultsArea.classList.add('show');
    resultsContent.innerHTML = '<div class="loading"></div> Decompressing file...';
    
    try {
        const response = await fetch('/api/decompress', {
            method: 'POST',
            body: formData
        });
        
        if (response.ok) {
            // Get filename from Content-Disposition header
            const contentDisposition = response.headers.get('Content-Disposition');
            let filename = 'decompressed_file';
            if (contentDisposition) {
                const filenameMatch = contentDisposition.match(/filename="?(.+)"?/);
                if (filenameMatch) {
                    filename = filenameMatch[1];
                }
            }
            
            // Download the file
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = filename;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
            
            resultsContent.innerHTML = `
                <div class="result-card">
                    <div class="result-header" style="color: #28a745;">✅ Decompression Successful!</div>
                    <p style="text-align: center; margin-top: 15px; font-size: 16px;">
                        Your file has been decompressed and downloaded: <strong>${filename}</strong>
                    </p>
                    <div style="text-align: center; margin-top: 20px;">
                        <button onclick="location.reload()" style="padding: 12px 24px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; border-radius: 8px; cursor: pointer; font-size: 16px;">
                            🔄 Decompress Another File
                        </button>
                    </div>
                </div>
            `;
        } else {
            const error = await response.json();
            resultsContent.innerHTML = `
                <div class="result-card">
                    <div class="result-header" style="color: #dc3545;">❌ Decompression Failed</div>
                    <p style="text-align: center; margin-top: 15px; color: #dc3545;">
                        ${error.error || 'Unknown error occurred'}
                    </p>
                </div>
            `;
        }
    } catch (error) {
        resultsContent.innerHTML = `
            <div class="result-card">
                <div class="result-header" style="color: #dc3545;">❌ Error</div>
                <p style="text-align: center; margin-top: 15px; color: #dc3545;">
                    ${error.message}
                </p>
            </div>
        `;
    }
}

function toggleDarkMode() {
    document.body.classList.toggle('dark-mode');
    const isDark = document.body.classList.contains('dark-mode');
    localStorage.setItem('darkMode', isDark);
    document.querySelector('.dark-mode-toggle').textContent = isDark ? '☀️' : '🌙';
}

// Load saved dark mode preference
if(localStorage.getItem('darkMode') === 'true') {
    document.body.classList.add('dark-mode');
    document.querySelector('.dark-mode-toggle').textContent = '☀️';
}
</script>
"""


@app.route('/')
def home():
    return render_template_string(HOME_PAGE)


@app.route('/text')
def text():
    return render_template_string(TEXT_PAGE)


@app.route('/images')
def images():
    return render_template_string(IMAGE_PAGE)


@app.route('/videos')
def videos():
    return render_template_string(VIDEO_PAGE)


@app.route('/documents')
def documents():
    return render_template_string(DOCUMENT_PAGE)


# History and Reports Routes
@app.route('/history')
def history():
    """Display compression history"""
    from utils.database import get_db
    db = get_db()
    history_data = db.get_compression_history(limit=100)
    statistics = db.get_statistics()
    
    return render_template_string(HISTORY_PAGE, history=history_data, stats=statistics)


@app.route('/decompress')
def decompress():
    """Display decompression page"""
    return render_template_string(DECOMPRESS_PAGE)


@app.route('/api/decompress', methods=['POST'])
def api_decompress():
    """API endpoint for file decompression"""
    import pickle
    import os
    from algorithms.rle import decompress as rle_decompress
    from algorithms.huffman import decompress_from_bytes as huffman_decompress
    from algorithms.lzw import decompress as lzw_decompress
    
    try:
        # Get uploaded file and algorithm
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        algorithm = request.form.get('algorithm')
        
        if not file or not file.filename or file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not algorithm:
            return jsonify({'error': 'No algorithm selected'}), 400
        
        # Read the compressed data
        file_content = file.stream.read()
        
        # Decompress based on algorithm
        if algorithm == 'rle':
            compressed_data = pickle.loads(file_content)
            decompressed = rle_decompress(compressed_data)
        elif algorithm == 'huffman':
            # Huffman uses decompress_from_bytes which handles pickle internally
            decompressed = huffman_decompress(file_content)
        elif algorithm == 'lzw':
            compressed_data = pickle.loads(file_content)
            decompressed = lzw_decompress(compressed_data)
        else:
            return jsonify({'error': f'Unknown algorithm: {algorithm}'}), 400
        
        # Determine output filename
        original_filename = file.filename.replace('.pkl', '') if file.filename else 'decompressed'
        if original_filename.endswith('_compressed'):
            original_filename = original_filename.replace('_compressed', '_decompressed')
        else:
            original_filename = f'decompressed_{original_filename}'
        
        # Create response with decompressed data
        output = io.BytesIO()
        
        # Check if decompressed data is text or binary
        if isinstance(decompressed, str):
            output.write(decompressed.encode('utf-8'))
            if not original_filename.endswith('.txt'):
                original_filename += '.txt'
        elif isinstance(decompressed, list):
            # LZW and Huffman might return list - join it
            if all(isinstance(item, str) for item in decompressed):
                output.write(''.join(decompressed).encode('utf-8'))
                if not original_filename.endswith('.txt'):
                    original_filename += '.txt'
            else:
                # Binary data as list of integers
                output.write(bytes(decompressed))
        elif isinstance(decompressed, bytes):
            output.write(decompressed)
        else:
            # If it's another type, try to pickle it
            pickle.dump(decompressed, output)
            if not original_filename.endswith('.pkl'):
                original_filename += '.pkl'
        
        output.seek(0)
        
        return send_file(
            output,
            as_attachment=True,
            download_name=original_filename,
            mimetype='application/octet-stream'
        )
        
    except pickle.UnpicklingError as e:
        return jsonify({'error': f'Invalid compressed file format: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': f'Decompression failed: {str(e)}'}), 500


@app.route('/api/history')
def api_history():
    """API endpoint for compression history"""
    from utils.database import get_db
    db = get_db()
    
    file_type = request.args.get('file_type')
    algorithm = request.args.get('algorithm')
    limit = int(request.args.get('limit', 50))
    
    history_data = db.get_compression_history(limit=limit, file_type=file_type, algorithm=algorithm)
    return jsonify({'history': history_data})


@app.route('/api/statistics')
def api_statistics():
    """API endpoint for compression statistics"""
    from utils.database import get_db
    db = get_db()
    statistics = db.get_statistics()
    return jsonify(statistics)


@app.route('/download/original/<file_id>')
def download_original(file_id):
    """Download original file"""
    from utils.database import get_db
    db = get_db()
    
    file_data = db.get_file(file_id)
    metadata = db.get_file_metadata(file_id)
    
    if file_data and metadata:
        filename = metadata.get('filename', 'original_file')
        return send_file(
            io.BytesIO(file_data),
            as_attachment=True,
            download_name=filename
        )
    return jsonify({'error': 'File not found'}), 404


@app.route('/download/compressed/dat/<file_id>')
def download_compressed_dat(file_id):
    """Download compressed file as .dat (raw binary format)"""
    from utils.database import get_db
    
    db = get_db()
    
    file_data = db.get_file(file_id)
    metadata = db.get_file_metadata(file_id)
    
    if not file_data or not metadata:
        return jsonify({'error': 'File not found'}), 404
    
    original_filename = metadata.get('filename', 'compressed_file')
    algorithm = metadata.get('algorithm', '').lower()
    
    # Change extension to .dat
    filename_without_ext = original_filename.rsplit('.', 1)[0] if '.' in original_filename else original_filename
    dat_filename = f"{filename_without_ext}_{algorithm}.dat"
    
    # Return raw compressed data as .dat file
    return send_file(
        io.BytesIO(file_data),
        as_attachment=True,
        download_name=dat_filename,
        mimetype='application/octet-stream'
    )


@app.route('/download/compressed/<file_id>')
def download_compressed(file_id):
    """Download compressed file"""
    from utils.database import get_db
    import pickle
    from algorithms import rle, huffman, lzw
    from PIL import Image
    import numpy as np
    
    db = get_db()
    
    file_data = db.get_file(file_id)
    metadata = db.get_file_metadata(file_id)
    
    if not file_data or not metadata:
        return jsonify({'error': 'File not found'}), 404
    
    algorithm = metadata.get('algorithm', '').lower()
    file_extension = metadata.get('file_extension', '')
    original_filename = metadata.get('filename', 'compressed_file')
    
    # For text files, decompress and return as readable text
    if file_extension in ['.txt', '']:
        try:
            compressed_obj = pickle.loads(file_data)
            
            # Decompress based on algorithm
            if algorithm == 'rle':
                decompressed = rle.decompress(compressed_obj.get('compressed', []))
            elif algorithm == 'huffman':
                encoded = compressed_obj.get('encoded', '')
                codes = compressed_obj.get('codes', {})
                decompressed = huffman.decompress(encoded, codes)
            elif algorithm == 'lzw':
                decompressed = lzw.decompress(compressed_obj.get('compressed', []))
            else:
                decompressed = str(compressed_obj)
            
            # Return as readable text file
            text_data = decompressed.encode('utf-8') if isinstance(decompressed, str) else bytes(decompressed) if isinstance(decompressed, (list, tuple)) else decompressed
            return send_file(
                io.BytesIO(text_data),
                as_attachment=True,
                download_name=original_filename,
                mimetype='text/plain'
            )
        except Exception as e:
            print(f"Error decompressing text: {e}")
    
    # For image files, decompress and return as image
    elif file_extension in ['.png', '.jpg', '.jpeg', '.bmp', '.gif']:
        try:
            compressed_obj = pickle.loads(file_data)
            
            # Get image metadata from the compressed data
            shape = compressed_obj.get('shape')
            mode = compressed_obj.get('mode', 'L')
            
            # Decompress based on algorithm
            if algorithm == 'rle':
                compressed_data = compressed_obj.get('compressed', [])
                decompressed = rle.decompress(compressed_data)
                # Convert back to image data
                data = [ord(c) if isinstance(c, str) else c for c in decompressed]
            elif algorithm == 'huffman':
                encoded = compressed_obj.get('encoded', '')
                codes = compressed_obj.get('codes', {})
                decompressed = huffman.decompress(encoded, codes)
                data = [ord(c) if isinstance(c, str) else c for c in decompressed]
            elif algorithm == 'lzw':
                compressed_data = compressed_obj.get('compressed', [])
                decompressed = lzw.decompress(compressed_data)
                data = [ord(c) if isinstance(c, str) else c for c in decompressed]
            else:
                return jsonify({'error': 'Unknown algorithm'}), 400
            
            # Reconstruct image
            if shape:
                img_array = np.array(data[:np.prod(shape)], dtype=np.uint8).reshape(shape)
                img = Image.fromarray(img_array, mode=mode)
                
                # Save to buffer
                img_buffer = io.BytesIO()
                img_format = file_extension[1:].upper()
                if img_format == 'JPG':
                    img_format = 'JPEG'
                img.save(img_buffer, format=img_format)
                img_buffer.seek(0)
                
                return send_file(
                    img_buffer,
                    as_attachment=True,
                    download_name=original_filename,
                    mimetype=f'image/{file_extension[1:]}'
                )
        except Exception as e:
            print(f"Error decompressing image: {e}")
    
    # For other files (video, documents), return the raw compressed data with proper extension
    # These will need to be decompressed using a separate tool
    return send_file(
        io.BytesIO(file_data),
        as_attachment=True,
        download_name=original_filename
    )


@app.route('/report/single/<record_id>')
def generate_single_report(record_id):
    """Generate PDF report for single compression"""
    from utils.database import get_db
    from utils.report_generator import get_report_generator
    
    db = get_db()
    history = db.get_compression_history(limit=1000)
    
    # Find the record
    record = None
    for h in history:
        if h.get('_id') == record_id:
            record = h
            break
    
    if record:
        report_gen = get_report_generator()
        pdf_buffer = report_gen.generate_single_compression_report(record)
        
        return send_file(
            pdf_buffer,
            as_attachment=True,
            download_name=f'compression_report_{record_id}.pdf',
            mimetype='application/pdf'
        )
    
    return jsonify({'error': 'Record not found'}), 404


@app.route('/report/history')
def generate_history_report():
    """Generate PDF report for compression history"""
    from utils.database import get_db
    from utils.report_generator import get_report_generator
    
    db = get_db()
    history_data = db.get_compression_history(limit=100)
    statistics = db.get_statistics()
    
    report_gen = get_report_generator()
    pdf_buffer = report_gen.generate_history_report(history_data, statistics)
    
    return send_file(
        pdf_buffer,
        as_attachment=True,
        download_name='compression_history_report.pdf',
        mimetype='application/pdf'
    )


@app.route('/api/delete/<record_id>', methods=['DELETE'])
def delete_record(record_id):
    """Delete a compression record"""
    from utils.database import get_db
    db = get_db()
    
    success = db.delete_record(record_id)
    if success:
        return jsonify({'message': 'Record deleted successfully'})
    return jsonify({'error': 'Failed to delete record'}), 500


if __name__ == '__main__':
    print("\n" + "="*60)
    print("  🌐 Data Compression Project - Separated Interface")
    print("="*60)
    print("\n📱 Starting web server...")
    print("🌍 Open your browser and go to: http://localhost:8080")
    print("⏹️  Press CTRL+C to stop the server\n")
    
    app.run(host='0.0.0.0', port=8080, debug=True)
