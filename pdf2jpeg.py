#!/usr/bin/env python3
import fitz  # PyMuPDF
import os
import glob
import argparse

def list_image_dpis(pdf_path):
    """
    For each raster image embedded in the PDF, print its pixel size and
    the display rectangle size (in points), then compute its effective DPI.
    """
    doc = fitz.open(pdf_path)
    print(f"\n--- Image DPI info for '{os.path.basename(pdf_path)}' ---")
    for page_num, page in enumerate(doc, start=1):
        images = page.get_images(full=True)
        if not images:
            continue
        print(f"Page {page_num}:")
        for img in images:
            xref = img[0]
            pix = fitz.Pixmap(doc, xref)
            w_px, h_px = pix.width, pix.height
            rects = page.get_image_rects(xref)
            for rect in rects:
                w_pt, h_pt = rect.width, rect.height
                # 1 point = 1/72 inch
                w_in = w_pt / 72
                h_in = h_pt / 72
                dpi_w = w_px / w_in if w_in else float('nan')
                dpi_h = h_px / h_in if h_in else float('nan')
                print(f"  • xref={xref}: {w_px}×{h_px}px in "
                      f"{w_pt:.1f}×{h_pt:.1f}pt → "
                      f"{dpi_w:.0f}×{dpi_h:.0f} DPI")
    doc.close()

def pdf_to_jpeg(pdf_path, dpi=72, output_folder=None):
    """
    Render each page of pdf_path to JPEG at the specified DPI.
    Default dpi=72. Higher DPI → higher resolution.
    Appends '<dpi>dpi' to the filename.
    """
    if output_folder is None:
        output_folder = os.path.dirname(pdf_path)
    os.makedirs(output_folder, exist_ok=True)

    dpi_value = int(dpi)
    zoom = dpi / 72
    doc = fitz.open(pdf_path)
    base = os.path.splitext(os.path.basename(pdf_path))[0]
    mat = fitz.Matrix(zoom, zoom)

    for i, page in enumerate(doc, start=1):
        pix = page.get_pixmap(matrix=mat)
        out_name = f"{base}_page{i}_{dpi_value}dpi.jpg"
        out_path = os.path.join(output_folder, out_name)
        pix.save(out_path)
        print(f"Saved: {out_path}")
    doc.close()

def process_pdf(pdf_path, dpi, output_folder):
    print(f"\n=== Processing '{pdf_path}' at {int(dpi)} DPI ===")
    list_image_dpis(pdf_path)
    pdf_to_jpeg(pdf_path, dpi=dpi, output_folder=output_folder)

def main():
    parser = argparse.ArgumentParser(
        description="Convert PDF pages to JPEG (filename includes DPI) and list embedded-image DPIs."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--file", help="Path to a single PDF file")
    group.add_argument("--dir",  help="Path to a directory of PDF files")
    parser.add_argument(
        "--dpi",
        type=int,
        default=72,
        help="DPI for rendering (default: 72, common values: 150, 300, 600)"
    )
    parser.add_argument(
        "--output",
        help="Directory to save JPEGs (defaults to each PDF’s folder)"
    )
    args = parser.parse_args()

    if args.file:
        process_pdf(args.file, dpi=args.dpi, output_folder=args.output)
    else:
        pdfs = glob.glob(os.path.join(args.dir, "*.pdf"))
        if not pdfs:
            print(f"No PDF files found in directory: {args.dir}")
            return
        for pdf in pdfs:
            process_pdf(pdf, dpi=args.dpi, output_folder=args.output)

if __name__ == "__main__":
    main()
