# Separated Architecture Documentation

## Overview

The project has been reorganized with a **separated architecture** where:
- **Each algorithm** (RLE, Huffman, LZW) has its own dedicated route file
- **Each file type** (Images, Videos, Documents) has its own dedicated page
- All components work independently and can be easily maintained

## New File Structure

```
DataCompressionProject/
├── algorithms/              # Original algorithm implementations
│   ├── rle.py              # Run Length Encoding
│   ├── huffman.py          # Huffman Coding
│   └── lzw.py              # LZW Compression
│
├── routes/                 # NEW: Separate route files for each algorithm
│   ├── __init__.py         # Routes package initializer
│   ├── rle_routes.py       # RLE compression endpoints
│   ├── huffman_routes.py   # Huffman compression endpoints
│   └── lzw_routes.py       # LZW compression endpoints
│
├── handlers/               # File type handlers
│   ├── image_handler.py
│   ├── video_handler.py
│   └── document_handler.py
│
├── app_separated.py        # NEW: Main application with separated pages
├── web_ui.py              # Original web interface (still functional)
└── ...

```

## Algorithm Route Files

### 1. `routes/rle_routes.py`
Contains all RLE compression endpoints:
- `/rle/compress/text` - Compress text
- `/rle/compress/image` - Compress images
- `/rle/compress/video` - Compress videos
- `/rle/compress/document` - Compress documents

### 2. `routes/huffman_routes.py`
Contains all Huffman compression endpoints:
- `/huffman/compress/text` - Compress text
- `/huffman/compress/image` - Compress images
- `/huffman/compress/video` - Compress videos
- `/huffman/compress/document` - Compress documents

### 3. `routes/lzw_routes.py`
Contains all LZW compression endpoints:
- `/lzw/compress/text` - Compress text
- `/lzw/compress/image` - Compress images
- `/lzw/compress/video` - Compress videos
- `/lzw/compress/document` - Compress documents

## Separated Pages

### Home Page (`/`)
- Overview of the project
- Links to all file type pages
- Algorithm descriptions
- Supported file formats

### Image Compression Page (`/images`)
- Upload area for image files
- Support for: PNG, JPG, JPEG, BMP, GIF
- Grayscale conversion option
- Individual algorithm compression buttons
- "Compare All" feature for side-by-side comparison

### Video Compression Page (`/videos`)
- Upload area for video files
- Support for: MP4, AVI, MOV
- Grayscale conversion option
- Individual algorithm compression buttons
- "Compare All" feature for side-by-side comparison

### Document Compression Page (`/documents`)
- Upload area for document files
- Support for: TXT, PDF, DOCX, CSV
- Individual algorithm compression buttons
- "Compare All" feature for side-by-side comparison

## Running the Separated Application

### Start the new separated interface:
```bash
python app_separated.py
```

Then open: **http://localhost:8080**

### Or use the original interface:
```bash
python web_ui.py
```

## Benefits of Separated Architecture

### 1. **Better Organization**
- Each algorithm has its own file, making it easy to find and modify
- Each file type has its own dedicated page with appropriate UI

### 2. **Easy Maintenance**
- Update one algorithm without affecting others
- Modify one page type without touching others
- Clear separation of concerns

### 3. **Scalability**
- Easy to add new algorithms (just create a new route file)
- Easy to add new file types (just create a new page)
- Modular structure allows independent testing

### 4. **Code Reusability**
- Each route file follows the same pattern
- Easy to understand and replicate
- Consistent API across all endpoints

### 5. **Independent Testing**
- Test each algorithm independently
- Test each file type independently
- Easier debugging and troubleshooting

## API Endpoints

All endpoints accept POST requests and return JSON responses.

### Request Format (File Upload)
```javascript
FormData {
  file: <File>,
  grayscale: 'true' | 'false'  // For images/videos only
}
```

### Response Format
```json
{
  "algorithm": "RLE|Huffman|LZW",
  "file_type": "image|video|document",
  "original_size": 12345,
  "compressed_size": 6789,
  "compression_ratio": 0.5500,
  "space_savings": 45.00,
  "compression_time": 0.001234,
  "decompression_time": 0.000567,
  "is_correct": true,
  "metadata": { ... }
}
```

## Navigation

The application features a persistent navigation bar on all pages:
- 🏠 Home
- 🖼️ Images
- 🎥 Videos
- 📄 Documents

Users can easily switch between file types without losing context.

## Features on Each Page

### Upload Area
- Click to upload or drag-and-drop
- File type validation
- File size display

### Compression Options
- Individual algorithm buttons (RLE, Huffman, LZW)
- "Compare All Algorithms" button
- Grayscale option (images/videos)

### Results Display
- Detailed metrics for each algorithm
- Visual comparison when using "Compare All"
- Data integrity verification
- Color-coded success/error indicators

## Comparison with Original Structure

### Before (web_ui.py)
- Single file with all routes
- Mixed UI for all file types
- Harder to maintain and extend

### After (app_separated.py + routes/)
- Separate route files for each algorithm
- Dedicated pages for each file type
- Clean, modular architecture
- Easy to maintain and extend

## Next Steps

### To add a new algorithm:
1. Create `routes/newalgo_routes.py`
2. Import and register blueprint in `app_separated.py`
3. Add button to each page template

### To add a new file type:
1. Create handler in `handlers/newtype_handler.py`
2. Add route in each algorithm file
3. Create new page template in `app_separated.py`
4. Add navigation button

## Backward Compatibility

The original `web_ui.py` is still functional and can be used if needed. Both applications can coexist, but they should not run on the same port simultaneously.

---

**Created:** November 2025  
**Version:** 2.0 - Separated Architecture
