from pathlib import Path
from io import BytesIO
from pypdf import PdfReader
from docx import Document as DocxDocument

def extract_text(filename: str, data: bytes) -> str:
    suffix = Path(filename).suffix.lower()
    if suffix == ".pdf":
        reader = PdfReader(BytesIO(data))
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    if suffix == ".docx":
        doc = DocxDocument(BytesIO(data))
        return "\n".join(p.text for p in doc.paragraphs)
    if suffix in {".txt", ".md"}:
        return data.decode("utf-8", errors="replace")
    raise ValueError("Supported formats: PDF, DOCX, TXT, MD")

def chunk_text(text: str, size: int = 900, overlap: int = 120) -> list[str]:
    clean = " ".join(text.split())
    if not clean:
        return []
    chunks = []
    start = 0
    while start < len(clean):
        end = min(len(clean), start + size)
        chunks.append(clean[start:end])
        if end == len(clean):
            break
        start = max(start + 1, end - overlap)
    return chunks
