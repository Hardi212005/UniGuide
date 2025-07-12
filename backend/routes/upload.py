import os
from typing import List
from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import JSONResponse

from backend.utils.pdf_loader import load_pdf_as_documents
from backend.utils.embedding import embed_and_store_documents

router = APIRouter()

BASE_UPLOAD_DIR = os.path.join("backend", "data", "pdfs")

@router.post("/upload/")
async def upload_pdfs(
    files: List[UploadFile] = File(...), 
    category: str = Form(...)
):
    """
    Upload PDFs to a given category and store embedded chunks in ChromaDB.
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
            # Save PDF to disk
            file_path = os.path.join(category_dir, file.filename)
            with open(file_path, "wb") as f:
                f.write(await file.read())

            # Load and parse the PDF with metadata
            documents = load_pdf_as_documents(file_path, category)

            # Store documents in ChromaDB
            embed_and_store_documents(documents)

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
