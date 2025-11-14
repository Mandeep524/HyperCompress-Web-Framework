"""
Text and document file handler for compression.
Supports TXT, PDF, DOCX, CSV formats.
"""

import os


def load_text_file(file_path, encoding='utf-8'):
    """
    Load text file.
    
    Args:
        file_path: Path to text file
        encoding: File encoding
        
    Returns:
        String content
    """
    with open(file_path, 'r', encoding=encoding) as f:
        content = f.read()
    return content


def save_text_file(content, file_path, encoding='utf-8'):
    """
    Save text to file.
    
    Args:
        content: Text content
        file_path: Path to save
        encoding: File encoding
    """
    with open(file_path, 'w', encoding=encoding) as f:
        f.write(content)


def load_pdf(file_path):
    """
    Load PDF file and extract text.
    
    Args:
        file_path: Path to PDF file
        
    Returns:
        Extracted text content
    """
    try:
        import PyPDF2
        
        text = ""
        with open(file_path, 'rb') as f:
            pdf_reader = PyPDF2.PdfReader(f)
            for page in pdf_reader.pages:
                text += page.extract_text()
        
        return text
    except ImportError:
        raise ImportError("PyPDF2 is required for PDF support. Install with: pip install PyPDF2")


def load_docx(file_path):
    """
    Load DOCX file and extract text.
    
    Args:
        file_path: Path to DOCX file
        
    Returns:
        Extracted text content
    """
    try:
        from docx import Document
        
        doc = Document(file_path)
        text = []
        
        for paragraph in doc.paragraphs:
            text.append(paragraph.text)
        
        return '\n'.join(text)
    except ImportError:
        raise ImportError("python-docx is required for DOCX support. Install with: pip install python-docx")


def prepare_for_compression(file_path):
    """
    Prepare document for compression.
    
    Args:
        file_path: Path to file
        
    Returns:
        Dictionary with text data and metadata
    """
    ext = os.path.splitext(file_path)[1].lower()
    
    if ext == '.txt':
        content = load_text_file(file_path)
    elif ext == '.pdf':
        content = load_pdf(file_path)
    elif ext == '.docx':
        content = load_docx(file_path)
    elif ext == '.csv':
        content = load_text_file(file_path)
    else:
        # Try to read as text
        try:
            content = load_text_file(file_path)
        except:
            raise ValueError(f"Unsupported file format: {ext}")
    
    return {
        'data': content,
        'format': ext,
        'original_size': os.path.getsize(file_path),
        'length': len(content)
    }


def reconstruct_document(doc_data):
    """
    Reconstruct document from compressed data.
    
    Args:
        doc_data: Dictionary with data and metadata
        
    Returns:
        Text content
    """
    return doc_data['data']
