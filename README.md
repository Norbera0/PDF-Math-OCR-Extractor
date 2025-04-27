# PDF Engineering Exam OCR Extractor

This repository contains a single script, `OCR_data.py`, which uses [pix2text](https://github.com/breezedeus/pix2text) and PyMuPDF to extract text and mathematical formulas from engineering exam PDFs. The script is designed to handle documents with watermarks or faded backgrounds using OpenCV preprocessing.

## Features
- Extracts both regular text and formulas from each page of a PDF
- Handles faded backgrounds and watermarks with adaptive thresholding
- Saves extracted text with page markers
- Shows progress information during processing
- (Optional) Can save preprocessed images for inspection

## Requirements
- Python 3.8+
- [pix2text](https://github.com/breezedeus/pix2text)
- PyMuPDF (`fitz`)
- numpy
- opencv-python
- Pillow
- argparse

Install all dependencies with:
```bash
pip install -r requirements.txt
```

## Usage

### Basic usage
```bash
python pdf2mathtext.py --pdf_path "path/to/your.pdf"
```

### Windows Unicode Fix
If you encounter a `UnicodeDecodeError` on Windows, run:
```powershell
$env:PYTHONUTF8=1
python OCR_data.py --pdf_path "path/to/your.pdf"
```

### Optional: Save Preprocessed Images
Uncomment the indicated lines in `OCR_data.py` to save preprocessed images for each page in a `preprocessed_images` folder.

## Output
- Extracted text is saved in the `extracted_text` directory, with page markers.

## License
Specify your license here (e.g., MIT, Apache 2.0, or remove this section if not needed). 
