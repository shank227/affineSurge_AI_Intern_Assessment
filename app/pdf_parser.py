from pathlib import Path
import fitz
import re

# Base directory
BASE_DIRECTORY = Path(__file__).resolve().parent.parent

# PDF Path
PDF_PATH = BASE_DIRECTORY / "data" / "ct200_manual.pdf"

# Open PDF
doc = fitz.open(PDF_PATH)

# Heading Pattern
heading_pattern = re.compile(
    r'^\d+(?:\.\d+)*\.?\s+.+'
)

# Store extracted nodes
nodes = []

current_heading = None
current_content = []

# Read PDF page by page
for page in doc:

    text = page.get_text()
    lines = text.split("\n")

    for line in lines:

        line = line.strip()

        # Skip empty lines
        if not line:
            continue

        # If the line is a heading
        if heading_pattern.match(line):

            # Save the previous node
            if current_heading:
                nodes.append({
                    "heading": current_heading,
                    "content": "\n".join(current_content)
                })

            # Start a new node
            current_heading = line
            current_content = []

        # Otherwise, it's content
        else:
            if current_heading:
                current_content.append(line)

# Save the last node
if current_heading:
    nodes.append({
        "heading": current_heading,
        "content": "\n".join(current_content)
    })

# Print extracted nodes
for node in nodes:

    print("=" * 70)

    print("Heading:")
    print(node["heading"])
    print()

    print("Content:")
    print(node["content"])
    print()

# Close PDF
doc.close()