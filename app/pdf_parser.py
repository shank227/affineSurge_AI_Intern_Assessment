import fitz  # PyMuPDF

pdf_path = "C:\\Users\\shash\\OneDrive\\Desktop\\intern_assement_task\\affineSurge_AI_Intern_Assessment\\data\\ct200_manual.pdf"

doc = fitz.open(pdf_path)

print(f"Total Pages: {len(doc)}\n")

for page_num, page in enumerate(doc, start=1):
    print(f"========== PAGE {page_num} ==========")
    print(page.get_text())
    print("\n")