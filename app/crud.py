from app.database import SessionLocal
from app.models import Document, Section


def save_document(filename, version, nodes):

    db = SessionLocal()

    document = Document(
        filename=filename,
        version=version
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    for node in nodes:

        section = Section(
            document_id=document.id,
            section_number=node["section_number"],
            title=node["title"],
            level=node["level"],
            parent_section=node["parent_section"],
            content=node["content"],
            content_hash=node["content_hash"]
        )

        db.add(section)

    db.commit()
    db.close()