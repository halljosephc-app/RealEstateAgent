#!/usr/bin/env python3
"""
OCR Script for Real Estate Document Processing

Extracts text from scanned PDF documents using Tesseract OCR.
Designed to work with any property folder structure.

Usage:
    python ocr_pdfs.py [input_folder]

    If no folder specified, uses current directory's input/ subfolder.

Requirements:
    pip install pdf2image pytesseract Pillow

    Windows: Install Tesseract from https://github.com/UB-Mannheim/tesseract/wiki
    macOS: brew install tesseract poppler
    Linux: apt-get install tesseract-ocr poppler-utils
"""

import os
import sys
import platform
from pathlib import Path

try:
    from pdf2image import convert_from_path
    import pytesseract
except ImportError:
    print("Missing dependencies. Install with:")
    print("  pip install pdf2image pytesseract Pillow")
    sys.exit(1)


def find_tesseract():
    """Find Tesseract executable based on OS."""
    if platform.system() == "Windows":
        # Common Windows install locations
        paths = [
            r'C:\Program Files\Tesseract-OCR\tesseract.exe',
            r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',
            os.path.expanduser(r'~\AppData\Local\Tesseract-OCR\tesseract.exe'),
        ]
        for p in paths:
            if os.path.exists(p):
                return p
        print("Warning: Tesseract not found in standard locations.")
        print("Install from: https://github.com/UB-Mannheim/tesseract/wiki")
        return None
    else:
        # macOS/Linux - tesseract should be in PATH
        return 'tesseract'


def find_poppler():
    """Find Poppler path for Windows (not needed on macOS/Linux)."""
    if platform.system() != "Windows":
        return None

    # Common Windows poppler locations
    paths = [
        r'C:\poppler\Library\bin',
        r'C:\poppler\bin',
        r'C:\Program Files\poppler\bin',
        os.path.expanduser(r'~\poppler\Library\bin'),
    ]

    # Also check for versioned folders
    poppler_base = r'C:\poppler'
    if os.path.exists(poppler_base):
        for item in os.listdir(poppler_base):
            candidate = os.path.join(poppler_base, item, 'Library', 'bin')
            if os.path.exists(candidate):
                return candidate
            candidate = os.path.join(poppler_base, item, 'bin')
            if os.path.exists(candidate):
                return candidate

    for p in paths:
        if os.path.exists(p):
            return p

    print("Warning: Poppler not found. PDF conversion may fail on Windows.")
    print("Download from: https://github.com/oschwartz10612/poppler-windows/releases")
    return None


def get_pdfs_to_process(input_folder):
    """Find all PDFs in the input folder, sorted by name."""
    input_path = Path(input_folder)

    if not input_path.exists():
        print(f"Error: Input folder not found: {input_folder}")
        sys.exit(1)

    # Find all PDFs recursively
    pdfs = list(input_path.glob('**/*.pdf')) + list(input_path.glob('**/*.PDF'))

    # Sort by path for consistent ordering
    pdfs.sort(key=lambda p: str(p).lower())

    return pdfs


def is_likely_scanned(pdf_path, poppler_path=None):
    """
    Heuristic to check if a PDF might be scanned (image-based).
    Returns True if the PDF has very little extractable text relative to page count.
    """
    try:
        import fitz  # PyMuPDF - optional dependency
        doc = fitz.open(pdf_path)
        total_text = ""
        for page in doc:
            total_text += page.get_text()
        doc.close()

        # If very little text per page, likely scanned
        chars_per_page = len(total_text) / max(1, doc.page_count)
        return chars_per_page < 100  # Threshold: less than 100 chars/page
    except:
        # If PyMuPDF not available, assume we should try OCR
        return True


def ocr_pdf(pdf_path, poppler_path=None):
    """Extract text from a PDF using OCR."""
    text_parts = []

    try:
        # Convert PDF to images
        if poppler_path:
            images = convert_from_path(str(pdf_path), poppler_path=poppler_path, dpi=300)
        else:
            images = convert_from_path(str(pdf_path), dpi=300)

        for i, image in enumerate(images, 1):
            text_parts.append(f"--- Page {i} ---")
            text = pytesseract.image_to_string(image)
            text_parts.append(text)

        return "\n".join(text_parts), len(images)

    except Exception as e:
        return f"ERROR: {str(e)}", 0


def main():
    # Determine input folder
    if len(sys.argv) > 1:
        base_dir = sys.argv[1]
    else:
        # Default: look for input/ in current directory
        base_dir = os.path.join(os.getcwd(), 'input')
        if not os.path.exists(base_dir):
            base_dir = os.getcwd()

    print(f"Scanning for PDFs in: {base_dir}")

    # Configure Tesseract
    tesseract_path = find_tesseract()
    if tesseract_path and platform.system() == "Windows":
        pytesseract.pytesseract.tesseract_cmd = tesseract_path

    # Configure Poppler (Windows only)
    poppler_path = find_poppler()

    # Find PDFs
    pdfs = get_pdfs_to_process(base_dir)

    if not pdfs:
        print("No PDF files found.")
        sys.exit(0)

    print(f"Found {len(pdfs)} PDF files")

    # Determine output location
    output_dir = Path(base_dir).parent if Path(base_dir).name == 'input' else Path(base_dir)
    extracted_dir = output_dir / 'extracted'
    extracted_dir.mkdir(exist_ok=True)

    output_file = extracted_dir / 'Scanned_Documents_OCR.txt'

    # Process each PDF
    with open(output_file, 'w', encoding='utf-8') as out:
        out.write("=" * 80 + "\n")
        out.write("SCANNED DOCUMENTS - OCR EXTRACTED TEXT\n")
        out.write("=" * 80 + "\n")
        out.write(f"Source folder: {base_dir}\n")
        out.write(f"Generated by: ocr_pdfs.py\n\n")

        processed = 0
        for pdf_path in pdfs:
            rel_path = pdf_path.relative_to(base_dir) if base_dir in str(pdf_path) else pdf_path.name
            print(f"Processing: {rel_path}...")

            out.write("=" * 80 + "\n")
            out.write(f"DOCUMENT: {pdf_path.name}\n")
            out.write(f"Path: {rel_path}\n")
            out.write("=" * 80 + "\n\n")

            text, pages = ocr_pdf(pdf_path, poppler_path)
            out.write(text)
            out.write("\n\n")

            if pages > 0:
                print(f"  Done - {pages} pages processed")
                processed += 1
            else:
                print(f"  Error or no pages")

    print(f"\nOCR complete!")
    print(f"  Processed: {processed}/{len(pdfs)} files")
    print(f"  Output: {output_file}")


if __name__ == "__main__":
    main()
