from pathlib import Path

from pypdf import PdfReader


def load_pdf(file_path: str):
    """
    Load a PDF file and extract text page by page.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"PDF file not found: {file_path}")

    try:
        reader = PdfReader(file_path)
        documents = []

        for page_number, page in enumerate(reader.pages, start=1):
            text = page.extract_text() or ""

            # Skip completely empty pages
            if text.strip():
                documents.append({
                    "text": text,
                    "page": page_number
                })

        if not documents:
            raise ValueError("No readable text found in the PDF.")

        return documents

    except Exception as e:
        raise ValueError(f"Error processing PDF: {str(e)}")