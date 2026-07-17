from app.database import SessionLocal
from app.models import Document, Section


def get_sections(version):

    db = SessionLocal()

    document = (
        db.query(Document)
        .filter(Document.version == version)
        .first()
    )

    if not document:
        db.close()
        return {}

    sections = (
        db.query(Section)
        .filter(Section.document_id == document.id)
        .all()
    )

    data = {}

    for section in sections:

        key = (
            section.section_number,
            section.title
        )

        data[key] = section

    db.close()

    return data


def compare_versions(version1, version2):

    old = get_sections(version1)
    new = get_sections(version2)

    result = {
        "changed": [],
        "unchanged": [],
        "new": [],
        "removed": []
    }

    for key, section in new.items():

        if key not in old:

            result["new"].append({
                "section": section.section_number,
                "title": section.title
            })

        else:

            if section.content_hash == old[key].content_hash:

                result["unchanged"].append({
                    "section": section.section_number,
                    "title": section.title
                })

            else:

                result["changed"].append({
                    "section": section.section_number,
                    "title": section.title
                })

    for key, section in old.items():

        if key not in new:

            result["removed"].append({
                "section": section.section_number,
                "title": section.title
            })

    return result