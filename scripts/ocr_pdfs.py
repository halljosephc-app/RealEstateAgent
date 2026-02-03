import os
from pdf2image import convert_from_path
import pytesseract
from pathlib import Path

# Configure paths
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
poppler_path = r'C:\poppler\poppler-24.08.0\Library\bin'

# PDFs to OCR (scanned documents)
base_dir = r'C:\Users\hallj\Documents\24374 Arcadia Street'
scanned_pdfs = [
    ('CCF_000129 (2).pdf', 'CCF Document'),
    ('2026 Termite Work/2026 Termite Work/Termite Completion Jan 26.pdf', '2026 Termite Completion (Jan 26)'),
    ('2026 Termite Work/2026 Termite Work/Termite Report Jan 26.pdf', '2026 Termite Report (Jan 26)'),
    ('2025 Termite Work/2025 Termite Work/Termite Report May 25.pdf', '2025 Termite Report (May 25)'),
    ('2025 Termite Work/2025 Termite Work/Rodent work completed june 2025.pdf', '2025 Rodent Work Completion (June 25)'),
    ('2025 Termite Work/2025 Termite Work/Termite Supplimental Report June 25.pdf', '2025 Termite Supplemental Report (June 25)'),
    ('2025 Termite Work/2025 Termite Work/Termite Completion June 25.pdf', '2025 Termite Completion (June 25)'),
]

output_file = os.path.join(base_dir, 'Scanned_Documents_OCR.txt')

with open(output_file, 'w', encoding='utf-8') as out:
    out.write("=" * 80 + "\n")
    out.write("24374 ARCADIA STREET - SCANNED DOCUMENTS (OCR EXTRACTED)\n")
    out.write("=" * 80 + "\n")
    out.write("Generated via Tesseract OCR\n\n")

    for pdf_rel_path, title in scanned_pdfs:
        pdf_path = os.path.join(base_dir, pdf_rel_path)
        print(f"Processing: {title}...")

        out.write("=" * 80 + "\n")
        out.write(f"DOCUMENT: {title}\n")
        out.write(f"File: {pdf_rel_path}\n")
        out.write("=" * 80 + "\n\n")

        try:
            # Convert PDF to images
            images = convert_from_path(pdf_path, poppler_path=poppler_path, dpi=300)

            for i, image in enumerate(images, 1):
                out.write(f"--- Page {i} ---\n")
                # OCR the image
                text = pytesseract.image_to_string(image)
                out.write(text)
                out.write("\n\n")

            print(f"  Done - {len(images)} pages processed")

        except Exception as e:
            out.write(f"ERROR processing this document: {str(e)}\n\n")
            print(f"  Error: {e}")

print(f"\nOCR complete! Output saved to: {output_file}")
