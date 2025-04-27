import fitz  # PyMuPDF
import numpy as np
import os
import argparse
from pix2text import Pix2Text
from PIL import Image
import cv2

"""
NOTE: On Windows, if you encounter UnicodeDecodeError, run this script with:
    $env:PYTHONUTF8=1; python OCR_data.py --pdf_path "sample.pdf"
This ensures all files are read as UTF-8.
"""

def extract_text_from_pdf(pdf_path):
    print(f"Processing: {pdf_path}")
    
    # Initialize Pix2Text
    p2t = Pix2Text()
    
    # Open the PDF
    doc = fitz.open(pdf_path)
    all_text = ""
    
    total_pages = len(doc)
    print(f"Total pages: {total_pages}")
    
    # Iterate through each page
    for page_num in range(total_pages):
        print(f"Processing page {page_num+1}/{total_pages}...")
        
        page = doc.load_page(page_num)
        
        # Convert page to image
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))  # Increase resolution for better recognition
        img_array = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.h, pix.w, pix.n)
        img = Image.fromarray(img_array)

        # Preprocess image to reduce faded backgrounds/watermarks
        # Convert PIL image to OpenCV format
        img_cv = np.array(img)
        if img_cv.shape[2] == 4:
            img_cv = cv2.cvtColor(img_cv, cv2.COLOR_RGBA2RGB)
        gray = cv2.cvtColor(img_cv, cv2.COLOR_RGB2GRAY)
        # Adaptive thresholding to remove light backgrounds
        processed = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                          cv2.THRESH_BINARY, 35, 15)
        # Convert back to PIL Image
        processed_img = Image.fromarray(processed)

        # Save the preprocessed image for inspection
        """
        os.makedirs('preprocessed_images', exist_ok=True)
        processed_img.save(f'preprocessed_images/page_{page_num+1}.png')
        """
        # Process with Pix2Text
        try:
            result = p2t.recognize(processed_img)
        except Exception as e:
            print(f"Error processing page {page_num+1}: {e}")
            result = "[Error extracting text from this page]"
        
        # Add page number for reference
        all_text += f"\n\n--- PAGE {page_num+1} ---\n\n{result}"
    
    return all_text

# Main execution
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract text and formulas from a PDF using pix2text.")
    parser.add_argument('--pdf_path', type=str, default="sample.pdf", help='Path to the PDF file to process.')
    parser.add_argument('--output_dir', type=str, default="extracted_text", help='Directory to save extracted text.')
    args = parser.parse_args()

    pdf_path = args.pdf_path
    output_dir = args.output_dir

    if not os.path.isfile(pdf_path):
        print(f"Error: File not found: {pdf_path}")
        exit(1)

    os.makedirs(output_dir, exist_ok=True)

    try:
        extracted_text = extract_text_from_pdf(pdf_path)
        
        # Save the extracted text
        filename = os.path.basename(pdf_path).replace(".pdf", "")
        output_path = os.path.join(output_dir, f"{filename}.txt")
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(extracted_text)
        
        print(f"Extraction complete! Text saved to: {output_path}")
    except Exception as e:
        print(f"Error occurred: {str(e)}")
