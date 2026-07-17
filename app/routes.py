from fastapi import APIRouter

from app.database import SessionLocal
from app.models import Document, Section
from sqlalchemy import or_
from app.versioning import compare_versions
from pydantic import BaseModel
from app.selection import save_selection

from app.llm import generate_questions
from app.output_store import save_output
import json
from pathlib import Path

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

@router.post("/generate/{selection_id}")
def generate(selection_id: int):

    base_dir = Path(__file__).resolve().parent.parent
    selection_file = base_dir / "data" / "selections.json"

    with open(selection_file, "r") as file:
        selections = json.load(file)

    selection = next(
        (s for s in selections if s["id"] == selection_id),
        None
    )

    if not selection:
        return {"message": "Selection not found"}

    db = SessionLocal()

    sections = (
        db.query(Section)
        .filter(Section.id.in_(selection["node_ids"]))
        .all()
    )

    context = ""

    for section in sections:
        context += f"\n{section.title}\n"
        context += section.content
        context += "\n"

    output = generate_questions(context)

    db.close()

    return save_output(selection_id, output)

@router.get("/generated/{selection_id}")
def get_generated_output(selection_id: int):

    base_dir = Path(__file__).resolve().parent.parent
    output_file = base_dir / "data" / "generated_outputs.json"

    with open(output_file, "r") as file:
        outputs = json.load(file)

    for output in outputs:
        if output["selection_id"] == selection_id:
            return output

    return {"message": "No generated output found"}

@router.get("/staleness/{selection_id}")
def check_staleness(selection_id: int):

    base_dir = Path(__file__).resolve().parent.parent
    selection_file = base_dir / "data" / "selections.json"

    with open(selection_file, "r") as file:
        selections = json.load(file)

    selection = next(
        (s for s in selections if s["id"] == selection_id),
        None
    )

    if not selection:
        return {"message": "Selection not found"}

    if selection["version"] == "v2":
        return {
            "selection_id": selection_id,
            "stale": False,
            "message": "Selection already uses the latest version."
        }

    comparison = compare_versions(
        selection["version"],
        "v2"
    )

    changed = []

    for node_id in selection["node_ids"]:

        db = SessionLocal()

        section = (
            db.query(Section)
            .filter(Section.id == node_id)
            .first()
        )

        db.close()

        if not section:
            continue

        for item in comparison["changed"]:
            if (
                item["section_number"] == section.section_number
                and item["title"] == section.title
            ):
                changed.append({
                    "section_number": section.section_number,
                    "title": section.title
                })

    return {
        "selection_id": selection_id,
        "stale": len(changed) > 0,
        "changed_nodes": changed
    }