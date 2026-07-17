import re

heading_pattern = re.compile(
    r'^\d+(?:\.\d+)*\.?\s+.+'
)

lines = [
    "1. Device Overview",
    "1.1 Intended Use",
    "2.1 General Specifications",
    "Random sentence",
    "Power source",
]

for line in lines:

    if heading_pattern.match(line):
        print("Heading:", line)

    else:
        print("Content:", line)