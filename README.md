# PDF to JPEG Converter & PDF Compressor

This repository provides two **separate utilities**:

1. [**PDF to JPEG Converter & Image DPI Lister**](#1-pdf-to-jpeg-converter--image-dpi-lister)
2. [**PDF Compressor (using Ghostscript)**](#2-pdf-compressor-ghostscript-based)

---

## 1. PDF to JPEG Converter & Image DPI Lister

This tool converts each page of a PDF file to JPEG images and lists the DPI (dots per inch) of all embedded raster images in the PDF.

### Features

- **Convert PDF pages to JPEG:** Each page is rendered as a JPEG file. You can control the output resolution using a zoom factor. Output filenames include the DPI (e.g., `file_page1_144dpi.jpg`).
- **List embedded image DPIs:** For each raster image in the PDF, the script prints its pixel size, display size (in points), and effective DPI.
- **Batch processing:** Process a single PDF or all PDFs in a directory.
- **Custom output folder:** Optionally specify an output directory for JPEGs.

### Requirements

- Python 3.x
- [PyMuPDF (fitz)](https://pymupdf.readthedocs.io/en/latest/)

Install dependencies:

```bash
pip install pymupdf
```

### Usage

```bash
python pdf2jpeg.py --file <PDF_FILE> [--zoom <factor>] [--output <output_dir>]
python pdf2jpeg.py --dir <PDF_DIR> [--zoom <factor>] [--output <output_dir>]
```

#### Arguments

- `--file`: Path to a single PDF file to process.
- `--dir`: Path to a directory containing PDF files (processes all `.pdf` files in the directory).
- `--zoom`: (Optional) Zoom factor for rendering.  
  - `1.00` = 72 DPI (default)
  - `4.17` ≈ 300 DPI (300/72)
  - `8.33` ≈ 600 DPI (600/72)
  - Higher values = higher resolution.
- `--output`: (Optional) Directory to save JPEGs.  
  - Defaults to the folder of each PDF.

#### Example

Convert a single PDF at 144 DPI and save JPEGs to `output/`:

```bash
python pdf2jpeg.py --file mydoc.pdf --zoom 2.0 --output output/
```

Process all PDFs in a folder at 300 DPI:

```bash
python pdf2jpeg.py --dir ./pdfs/ --zoom 4.17
```

#### Output

- JPEG images are saved as `<PDFNAME>_page<N>_<DPI>dpi.jpg`.
- For each PDF, the script prints DPI info for all embedded images.

---

**Note:** Only raster images embedded in the PDF are analyzed for DPI. Vector graphics are not included in the DPI listing.

---

## 2. PDF Compressor (Ghostscript-based)

This is a separate utility to compress PDF files using Ghostscript with selectable quality/size presets.

### Requirements

- [Ghostscript](https://ghostscript.com/) (must be installed and available in your system PATH)

### Usage

```bash
python compress_pdf.py in.pdf out.pdf [preset]
```

- `preset` options (affect output PDF size and image quality):
  - `screen`   - lowest quality, smallest size (~72 dpi images)
  - `ebook`    - medium quality, small size (~150 dpi images) [default]
  - `printer`  - high quality, larger size (~300 dpi images)
  - `prepress` - maximum quality, largest size
  - `default`  - sensible middle-ground

**Example:**

```bash
python compress_pdf.py input.pdf output.pdf ebook
```

#### Output

- Compressed PDFs are saved to the specified output path.

---

**Note:** Ghostscript must be installed and available in your system PATH for PDF compression.