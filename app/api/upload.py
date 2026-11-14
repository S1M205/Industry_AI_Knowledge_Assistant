from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.models import Document
from app.services.chunk_service import split_documents
from app.services.document_service import load_pdf
from app.services.vector_service import create_vector_store


router = APIRouter()

UPLOAD_DIR = Path("data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@router.post("/upload")
async def upload_pdf(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Upload, process, and index a PDF document.
    """

    # Validate file type
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed."
        )

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Filename is missing."
        )

    # Create a unique filename to avoid overwriting files
    unique_filename = f"{uuid4()}_{file.filename}"
    file_path = UPLOAD_DIR / unique_filename

    try:
        # Save uploaded file
        content = await file.read()
        file_path.write_bytes(content)

        # Extract PDF text
        documents = load_pdf(str(file_path))

        # Split text into chunks
        chunks = split_documents(documents)

        # Add source metadata to every chunk
        for chunk in chunks:
            chunk["source"] = file.filename

        # Create vector store
        vectors = create_vector_store(chunks)

        # Save document metadata in PostgreSQL
        document = Document(
            filename=file.filename,
            pages=len(documents),
            chunks=len(chunks)
        )

        db.add(document)
        db.commit()
        db.refresh(document)

        return {
            "document_id": document.id,
            "filename": document.filename,
            "pages": document.pages,
            "chunks": document.chunks,
            "vectors": vectors,
            "message": "PDF uploaded and processed successfully."
        }

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="An error occurred while processing the document."
        )

    finally:
        await file.close()