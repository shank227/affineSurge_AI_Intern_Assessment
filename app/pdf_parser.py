from pathlib import Path
import fitz

BASE_DIRECTORY = Path(__file__).resolve().parent.parent
PDF_PATH = BASE_DIRECTORY / "data" / "ct200_manual.pdf"

doc = fitz.open(PDF_PATH)

print(f"Total Pages: {len(doc)}\n")

for page_num, page in enumerate(doc, start=1):
    print(f"========== PAGE {page_num} ==========")
    print(page.get_text())
    print("\n")
