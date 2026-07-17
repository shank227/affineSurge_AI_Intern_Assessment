from pathlib import Path
import fitz
import re


BASE_DIRECTORY = Path(__file__).resolve().parent.parent
PDF_PATH = BASE_DIRECTORY / "data" / "ct200_manual.pdf"

heading_pattern = re.compile(
    r'^\d+(?:\.\d+)*\.?\s+.+'
)


def parse_heading(heading):
    parts = heading.split(" ", 1)

    section_number = parts[0].rstrip(".")
    title = parts[1] if len(parts) > 1 else ""

    level = len(section_number.split("."))

    if "." in section_number:
        parent_section = ".".join(section_number.split(".")[:-1])
    else:
        parent_section = None

    return {
        "section_number": section_number,
        "title": title,
        "level": level,
        "parent_section": parent_section
    }


doc = fitz.open(PDF_PATH)

nodes = []

current_heading = None
current_content = []

for page in doc:

    text = page.get_text()
    lines = text.split("\n")

    for line in lines:

        line = line.strip()

        if not line:
            continue

        if heading_pattern.match(line):

            if current_heading:

                heading_info = parse_heading(current_heading)

                nodes.append({
                    "section_number": heading_info["section_number"],
                    "title": heading_info["title"],
                    "level": heading_info["level"],
                    "parent_section": heading_info["parent_section"],
                    "content": "\n".join(current_content)
                })

            current_heading = line
            current_content = []

        else:

            if current_heading:
                current_content.append(line)

if current_heading:

    heading_info = parse_heading(current_heading)

    nodes.append({
        "section_number": heading_info["section_number"],
        "title": heading_info["title"],
        "level": heading_info["level"],
        "parent_section": heading_info["parent_section"],
        "content": "\n".join(current_content)
    })

doc.close()


for node in nodes:

    print("=" * 70)

    print(f"Section Number : {node['section_number']}")
    print(f"Title          : {node['title']}")
    print(f"Level          : {node['level']}")
    print(f"Parent Section : {node['parent_section']}")

    print("\nContent:")
    print(node["content"])
    print()