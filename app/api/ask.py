from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.services.llm_service import generate_answer
from app.services.vector_service import search_documents


router = APIRouter()


class Question(BaseModel):
    question: str = Field(
        ...,
        min_length=3,
        description="Question to ask about the uploaded documents."
    )


@router.post("/ask")
async def ask_question(data: Question):
    """
    Answer a question using the uploaded document context.
    """

    question = data.question.strip()

    if not question:
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
        )

    try:
        # Retrieve top relevant chunks
        results = search_documents(question, k=3)

        if not results:
            raise HTTPException(
                status_code=404,
                detail="No documents available. Please upload a PDF first."
            )

        # Create context from retrieved chunks
        context = "\n\n".join(
            result["text"] for result in results
        )

        # Generate answer using Groq
        answer = generate_answer(question, context)

        # Create unique source citations
        sources = []
        seen = set()

        for result in results:
            source = result.get("source", "Unknown")
            page = result.get("page", "Unknown")

            key = (source, page)

            if key not in seen:
                sources.append({
                    "source": source,
                    "page": page
                })
                seen.add(key)

        return {
            "question": question,
            "answer": answer,
            "sources": sources
        }

    except HTTPException:
        raise

    except RuntimeError as e:
        raise HTTPException(
            status_code=503,
            detail=str(e)
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred while answering the question."
        )