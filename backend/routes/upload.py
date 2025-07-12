import os
from typing import List
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse

from backend.utils.pdf_loader import extract_text_from_pdf
from backend.utils.embedding import store_pdf_text

router = APIRouter()

BASE_UPLOAD_DIR = os.path.join("backend", "data", "pdfs")

@router.post("/upload/")
async def upload_pdfs(
    files: List[UploadFile] = File(...), 
    category: str = Form(...)
):
    """
    Upload multiple PDFs to a category and store them in ChromaDB with metadata.
    """
    category_dir = os.path.join(BASE_UPLOAD_DIR, category)
    os.makedirs(category_dir, exist_ok=True)

    failed_files = []

    for file in files:
        if not file.filename.endswith(".pdf"):
            failed_files.append({
                "file": file.filename,
                "error": "Not a PDF"
            })
            continue

        try:
            # Save PDF to category-specific directory
            file_path = os.path.join(category_dir, file.filename)
            with open(file_path, "wb") as f:
                f.write(await file.read())

            # Extract text from PDF
            text = extract_text_from_pdf(file_path)

            # Add metadata: file name and category
            metadata = {
                "file_name": file.filename,
                "category": category
            }

            # Store with metadata
            store_pdf_text(text=text, file_name=file.filename, category=category, metadata=metadata)

        except Exception as e:
            failed_files.append({
                "file": file.filename,
                "error": str(e)
            })

    if failed_files:
        return JSONResponse(
            status_code=207,
            content={
                "message": "Some PDFs failed to upload or process.",
                "failed": failed_files
            }
        )

    return JSONResponse({
        "message": "All PDFs uploaded and processed successfully!"
    })
