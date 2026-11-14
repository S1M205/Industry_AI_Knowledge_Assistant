import logging
import os

from dotenv import load_dotenv
from groq import Groq


load_dotenv()

logger = logging.getLogger(__name__)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in .env file")


client = Groq(api_key=GROQ_API_KEY)


def generate_answer(question: str, context: str) -> str:
    """
    Generate an answer using the retrieved document context.
    """

    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an AI Knowledge Assistant. "
                        "Answer questions using only the provided document context. "
                        "If the answer is not available in the context, say: "
                        "'I don't have enough information in the uploaded document.'"
                    ),
                },
                {
                    "role": "user",
                    "content": f"""Context:
{context}

Question: {question}

Give a clear and concise answer."""
                },
            ],
            temperature=0.2,
        )

        answer = response.choices[0].message.content

        if not answer:
            raise RuntimeError("Empty response received from the LLM.")

        return answer.strip()

    except Exception as e:
        logger.exception("LLM generation failed")
        raise RuntimeError(
            "Unable to generate an answer. Please try again later."
        ) from e