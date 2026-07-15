#!/usr/bin/env python3
import subprocess
import sys
import shutil
import argparse

def compress_pdf(input_path: str, output_path: str, setting: str = '/ebook'):
    """
    Uses Ghostscript to compress a PDF.
    
    PDFSETTINGS:
      /screen   — lowest quality, ~72 dpi images
      /ebook    — medium quality, ~150 dpi images
      /printer  — high quality, ~300 dpi images
      /prepress — maximum quality
      /default  — a sensible middle-ground
    """
    if not shutil.which("gs"):
        print("ERROR: Ghostscript (‘gs’) not found in PATH.", file=sys.stderr)
        sys.exit(1)

    args = [
        "gs",
        "-sDEVICE=pdfwrite",
        "-dCompatibilityLevel=1.4",
        f"-dPDFSETTINGS={setting}",
        "-dNOPAUSE",
        "-dBATCH",
        "-dQUIET",
        f"-sOutputFile={output_path}",
        input_path
    ]
    try:
        subprocess.run(args, check=True)
        print(f"✔ Compressed '{input_path}' → '{output_path}' using {setting}")
    except subprocess.CalledProcessError as e:
        print("ERROR: Ghostscript failed:", e, file=sys.stderr)
        sys.exit(1)

def dpi_to_setting(dpi: int) -> str:
    """Convert DPI value to appropriate Ghostscript PDFSETTINGS."""
    if dpi <= 72:
        return "/screen"
    elif dpi <= 150:
        return "/ebook"
    elif dpi <= 300:
        return "/printer"
    else:
        return "/prepress"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Compress PDF files using Ghostscript with quality presets or DPI settings."
    )
    parser.add_argument("input", help="Input PDF file path")
    parser.add_argument("output", help="Output PDF file path")
    
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--preset",
        choices=["screen", "ebook", "printer", "prepress", "default"],
        default="ebook",
        help=(
            "Quality preset (default: ebook):\n"
            "  screen   - lowest quality, smallest size (~72 dpi images)\n"
            "  ebook    - medium quality, small size (~150 dpi images)\n"
            "  printer  - high quality, larger size (~300 dpi images)\n"
            "  prepress - maximum quality, largest size\n"
            "  default  - sensible middle-ground"
        )
    )
    group.add_argument(
        "--dpi",
        type=int,
        help=(
            "Target DPI for images (alternative to --preset):\n"
            "  ≤72   → screen quality\n"
            "  ≤150  → ebook quality\n"
            "  ≤300  → printer quality\n"
            "  >300  → prepress quality"
        )
    )
    
    args = parser.parse_args()
    
    if args.dpi:
        setting = dpi_to_setting(args.dpi)
        print(f"Using DPI {args.dpi} → {setting} quality")
    else:
        setting_map = {
            "screen":   "/screen",
            "ebook":    "/ebook",
            "printer":  "/printer",
            "prepress": "/prepress",
            "default":  "/default",
        }
        setting = setting_map[args.preset]
        print(f"Using preset '{args.preset}' → {setting} quality")
    
    compress_pdf(args.input, args.output, setting)
