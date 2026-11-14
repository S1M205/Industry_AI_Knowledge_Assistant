import logging

from fastapi import FastAPI

from app.api.ask import router as ask_router
from app.api.upload import router as upload_router
from app.services.vector_service import load_vector_store


# Configure application logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# Create FastAPI application
app = FastAPI(
    title="Industry AI Knowledge Assistant",
    description=(
        "A RAG-based AI assistant for uploading and querying PDF documents."
    ),
    version="1.0.0"
)


# Load saved vector data when the application starts
load_vector_store()


# Register API routes
app.include_router(upload_router)
app.include_router(ask_router)


@app.get("/", tags=["Health"])
def health_check():
    """Check whether the application is running."""

    return {
        "message": "Industry AI Knowledge Assistant is running",
        "status": "healthy"
    }