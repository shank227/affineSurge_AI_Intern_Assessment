from pathlib import Path

from app.pdf_parser import parse_pdf

BASE_DIRECTORY = Path(__file__).resolve().parent

parse_pdf(
    BASE_DIRECTORY / "data" / "ct200_manual.pdf",
    "ct200_manual.pdf",
    "v1"
)

parse_pdf(
    BASE_DIRECTORY / "data" / "ct200_manual_v2.pdf",
    "ct200_manual.pdf",
    "v2"
)

print("Both document versions imported successfully!")