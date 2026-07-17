from app.database import SessionLocal
from app.models import Document, Section

db = SessionLocal()

print("\nDocuments:")
for doc in db.query(Document).all():
    print(doc.id, doc.filename, doc.version)

print("\nSections:")
sections = db.query(Section).limit(5).all()

for section in sections:
    print("-" * 50)
    print("ID:", section.id)
    print("Section:", section.section_number)
    print("Title:", section.title)
    print("Hash:", section.content_hash[:12] + "...")