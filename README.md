# CT-200 Document Processing & QA Test Case Generation System

## Overview

This project is a backend system for processing versioned technical PDF documents, reconstructing their hierarchical structure, comparing document versions, and generating AI-assisted QA test cases.

The system performs the following tasks:

- Parse PDF documents into a hierarchical tree structure
- Store document sections in a SQLite database
- Compare different document versions using content hashes
- Create version-pinned selections
- Generate QA test cases using the Groq LLM API
- Detect stale selections when newer document versions are available

---

## Tech Stack

- Python 3.10+
- FastAPI
- SQLAlchemy
- SQLite
- PyMuPDF (fitz)
- Groq API (Llama 3.1 8B Instant)

---

## Project Structure

```
project/
│
├── app/
│   ├── database.py
│   ├── llm.py
│   ├── output_store.py
│   ├── pdf_parser.py
│   ├── routes.py
│   ├── selection.py
│   └── versioning.py
│
├── data/
│   ├── generated_outputs.json
│   └── selections.json
│
├── ct200_manual.pdf
├── ct200_manual_v2.pdf
├── ingest.py
├── main.py
├── requirements.txt
└── README.md
```

---

# Installation

## 1. Clone the repository

```bash
git clone <repository-url>
cd <repository-name>
```

---

## 2. Create a virtual environment

Windows

```bash
python -m venv venv
venv\Scripts\activate
```

Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure the Groq API Key

Create a `.env` file in the project root.

```env
GROQ_API_KEY=your_api_key_here
```

---

# Running the Project

## Step 1 — Ingest Documents

Run the ingestion script to parse both PDF versions and populate the SQLite database.

```bash
python ingest.py
```

---

## Step 2 — Start the FastAPI Server

```bash
uvicorn main:app --reload
```

Server runs at:

```
http://127.0.0.1:8000
```

---

## Step 3 — Open Swagger UI

Interactive API documentation:

```
http://127.0.0.1:8000/docs
```

---

# Available APIs

| Endpoint | Description |
|-----------|-------------|
| GET /sections | List top-level sections |
| GET /node/{id} | Retrieve a section and its children |
| GET /search | Search document sections |
| GET /compare | Compare two document versions |
| POST /selection | Create a version-pinned selection |
| POST /generate/{selection_id} | Generate QA test cases using the selected content |
| GET /generated/{selection_id} | Retrieve generated QA test cases |
| GET /staleness/{selection_id} | Check whether a saved selection is stale |

---

# Project Workflow

```
PDF Upload
     │
     ▼
PDF Parsing (PyMuPDF)
     │
     ▼
Heading Detection
     │
     ▼
Hierarchy Reconstruction
     │
     ▼
SQLite Database
     │
     ├──────────────► Browse APIs
     │
     ├──────────────► Version Comparison
     │
     ├──────────────► Selection API
     │
     ├──────────────► LLM Generation (Groq)
     │
     ├──────────────► Retrieval API
     │
     └──────────────► Staleness Detection
```

---

# Notes

- The parser reconstructs document hierarchy using numbered headings.
- Content hashing (SHA-256) is used to detect changes between document versions.
- Selections are version-pinned to preserve traceability.
- Generated outputs are stored in JSON files for this prototype implementation.

---

# Future Improvements

- Replace JSON storage with a scalable NoSQL or relational database.
- Improve heading detection using layout-aware parsing (font size, spacing, indentation).
- Support OCR for scanned PDF documents.
- Implement authentication and user management.
- Store generated outputs directly in a database.

---

## Author

AI Engineering Internship Assignment Submission