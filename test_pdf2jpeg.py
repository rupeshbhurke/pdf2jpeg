import os
import shutil
import fitz
import pytest
from pdf2jpeg import pdf_to_jpeg, list_image_dpis

# Suppress PyMuPDF DeprecationWarnings for cleaner test output
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning, module="fitz")

TEST_PDF = "sample.pdf"
OUTPUT_DIR = "test_output"

@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown():
    # Setup: create a simple PDF for testing
    doc = fitz.open()
    page = doc.new_page()
    rect = fitz.Rect(50, 50, 200, 200)
    page.insert_text(rect.tl, "Test PDF Page 1")
    doc.save(TEST_PDF)
    doc.close()
    yield
    # Teardown: remove test files
    if os.path.exists(TEST_PDF):
        os.remove(TEST_PDF)
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)

def test_pdf_to_jpeg_creates_images():
    pdf_to_jpeg(TEST_PDF, zoom=1.0, output_folder=OUTPUT_DIR)
    files = os.listdir(OUTPUT_DIR)
    assert any(f.endswith(".jpg") for f in files), "JPEG not created"

def test_pdf_to_jpeg_dpi_in_filename():
    pdf_to_jpeg(TEST_PDF, zoom=2.0, output_folder=OUTPUT_DIR)
    files = os.listdir(OUTPUT_DIR)
    assert any("_144dpi.jpg" in f for f in files), "DPI not in filename"

def test_list_image_dpis_runs_without_error(capsys):
    # Should not raise and should print output
    list_image_dpis(TEST_PDF)
    captured = capsys.readouterr()
    assert "Image DPI info" in captured.out or "Page" in captured.out