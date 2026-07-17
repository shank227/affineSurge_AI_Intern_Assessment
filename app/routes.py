from fastapi import APIRouter

from app.database import SessionLocal
from app.models import Document, Section
from sqlalchemy import or_
from app.versioning import compare_versions
from pydantic import BaseModel
from app.selection import save_selection

router = APIRouter()


@router.get("/sections")
def get_sections(version: str = "v2"):

    db = SessionLocal()

    document = (
        db.query(Document)
        .filter(Document.version == version)
        .first()
    )

    if not document:
        db.close()
        return {"message": "Version not found"}

    sections = (
        db.query(Section)
        .filter(
            Section.document_id == document.id,
            Section.level == 1
        )
        .all()
    )

    result = []

    for section in sections:

        result.append({
            "id": section.id,
            "section_number": section.section_number,
            "title": section.title
        })

    db.close()

    return result

@router.get("/node/{node_id}")
def get_node(node_id: int):

    db = SessionLocal()

    node = (
        db.query(Section)
        .filter(Section.id == node_id)
        .first()
    )

    if not node:
        db.close()
        return {"message": "Node not found"}

    children = (
        db.query(Section)
        .filter(
            Section.document_id == node.document_id,
            Section.parent_section == node.section_number
        )
        .all()
    )

    response = {
        "id": node.id,
        "section_number": node.section_number,
        "title": node.title,
        "content": node.content,
        "content_hash": node.content_hash,
        "children": [
            {
                "id": child.id,
                "section_number": child.section_number,
                "title": child.title
            }
            for child in children
        ]
    }

    db.close()

    return response

@router.get("/search")
def search(query: str):

    db = SessionLocal()

    sections = (
        db.query(Section)
        .filter(
            or_(
                Section.title.ilike(f"%{query}%"),
                Section.content.ilike(f"%{query}%")
            )
        )
        .all()
    )

    result = []

    for section in sections:
        result.append({
            "id": section.id,
            "section": section.section_number,
            "title": section.title
        })

    db.close()

    return result

@router.get("/compare")
def compare(version1: str, version2: str):

    return compare_versions(version1, version2)

class SelectionRequest(BaseModel):
    name: str
    version: str
    node_ids: list[int]

@router.post("/selection")
def create_selection(request: SelectionRequest):

    return save_selection(
        request.name,
        request.version,
        request.node_ids
    )
