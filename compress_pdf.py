#!/usr/bin/env python3
import subprocess
import sys
import shutil

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

if __name__ == "__main__":
    help_msg = (
        "Usage: python compress_pdf.py in.pdf out.pdf [preset]\n"
        "  Preset options (affect output PDF size and image quality):\n"
        "    screen   - lowest quality, smallest size (~72 dpi images)\n"
        "    ebook    - medium quality, small size (~150 dpi images) [default]\n"
        "    printer  - high quality, larger size (~300 dpi images)\n"
        "    prepress - maximum quality, largest size\n"
        "    default  - sensible middle-ground\n"
        "Example:\n"
        "  python compress_pdf.py input.pdf output.pdf ebook"
    )
    if len(sys.argv) not in (3,4):
        print(help_msg)
        sys.exit(1)

    in_pdf = sys.argv[1]
    out_pdf = sys.argv[2]
    preset = sys.argv[3] if len(sys.argv) == 4 else "ebook"
    setting_map = {
        "screen":   "/screen",
        "ebook":    "/ebook",
        "printer":  "/printer",
        "prepress": "/prepress",
        "default":  "/default",
    }
    if preset not in setting_map:
        print("Invalid preset. Choose one of:", ", ".join(setting_map), file=sys.stderr)
        print(help_msg)
        sys.exit(1)

    compress_pdf(in_pdf, out_pdf, setting_map[preset])
