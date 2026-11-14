# Industry AI Knowledge Assistant

A RAG-based AI application that allows users to upload PDF documents and ask questions based on the uploaded content.

The application uses semantic search to retrieve relevant information from documents and generates context-based answers using a Large Language Model (LLM).

## Features

- Upload PDF documents
- Extract text from PDF pages
- Split text into smaller chunks
- Generate embeddings using Sentence Transformers
- Store and search embeddings using FAISS
- Persistent vector storage
- Retrieve the top relevant document chunks
- Generate answers using Groq LLM
- Display source filename and page number with answers
- Store document metadata in PostgreSQL
- Basic error handling and logging

## Architecture

```text
User Uploads PDF
       ↓
PDF Text Extraction
       ↓
Text Chunking
       ↓
Sentence Transformer Embeddings
       ↓
Persistent FAISS Vector Store
       ↓
PostgreSQL Metadata Storage
       ↓
User Asks a Question
       ↓
Top Relevant Chunks Retrieved
       ↓
Groq LLM
       ↓
Answer + Source Citation
```

## Tech Stack

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Sentence Transformers
- FAISS
- Groq API
- PyPDF
- NumPy

## Project Structure

```text
Industry_AI_Knowledge_Assistant/
│
├── app/
│   ├── api/
│   │   ├── ask.py
│   │   └── upload.py
│   │
│   ├── core/
│   │   ├── database.py
│   │   └── models.py
│   │
│   ├── services/
│   │   ├── chunk_service.py
│   │   ├── document_service.py
│   │   ├── llm_service.py
│   │   └── vector_service.py
│   │
│   └── main.py
│
├── data/
├── tests/
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Installation

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd Industry_AI_Knowledge_Assistant
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file based on `.env.example`.

Add your database URL and Groq API key:

```text
DATABASE_URL=your_postgresql_database_url
GROQ_API_KEY=your_groq_api_key
```

### 5. Run the application

```bash
python -m uvicorn app.main:app --reload
```

Open the API documentation:

```text
http://127.0.0.1:8000/docs
```

## API Endpoints

### POST `/upload`

Uploads and processes a PDF document.

The document is:

1. Saved locally
2. Converted into text
3. Split into chunks
4. Converted into embeddings
5. Stored in the FAISS vector store
6. Document metadata is saved in PostgreSQL

### POST `/ask`

Accepts a user question and:

1. Searches for the most relevant document chunks
2. Sends the retrieved context to the Groq LLM
3. Returns a context-based answer with source information

## Example Question

```json
{
  "question": "What are the skills mentioned in the resume?"
}
```

## Author

Sagar More