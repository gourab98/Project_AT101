# ocr_extract.py
import pytesseract
from pdf2image import convert_from_path
from PIL import Image, ImageFilter, ImageEnhance
import os
 
INPUT_DIR  = '/Users/gourabsaha/Downloads/Project_AT101/atguru-platform/data/raw_pdfs/'
OUTPUT_DIR = '/Users/gourabsaha/Downloads/Project_AT101/atguru-platform/data/extracted_text'
os.makedirs(OUTPUT_DIR, exist_ok=True)
 
def preprocess_image(img):
    """Improve image quality before OCR for better accuracy."""
    img = img.convert('L')                          # convert to greyscale
    img = ImageEnhance.Contrast(img).enhance(2.0)  # boost contrast
    img = img.filter(ImageFilter.SHARPEN)           # sharpen edges
    return img
 
def ocr_pdf(pdf_path, output_txt_path):
    print(f'Processing: {pdf_path}')
    # Convert each PDF page to a 300 DPI image
    pages = convert_from_path(pdf_path, dpi=300)
    full_text = ''
    for i, page in enumerate(pages):
        print(f'  Page {i+1}/{len(pages)}')
        page = preprocess_image(page)
        # 'ben' = Bengali language code for Tesseract
        text = pytesseract.image_to_string(page, lang='ben')
        full_text += text + '\n'
    with open(output_txt_path, 'w', encoding='utf-8') as f:
        f.write(full_text)
    print(f'  Saved to: {output_txt_path}')

    # Run on all PDFs in input folder
for filename in sorted(os.listdir(INPUT_DIR)):
    if filename.endswith('.pdf'):
        pdf_path = os.path.join(INPUT_DIR, filename)
        out_name = filename.replace('.pdf', '.txt')
        out_path = os.path.join(OUTPUT_DIR, out_name)
        if not os.path.exists(out_path):  # skip already processed
            ocr_pdf(pdf_path, out_path)

print('OCR complete!')