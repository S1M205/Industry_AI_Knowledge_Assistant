from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_documents(documents, chunk_size=500, chunk_overlap=50):
    """
    Split extracted PDF pages into smaller chunks
    while preserving page metadata.
    """

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ". ", " ", ""]
    )

    chunks = []

    for document in documents:
        text = document["text"]
        page_number = document["page"]

        if not text.strip():
            continue

        text_chunks = splitter.split_text(text)

        for chunk in text_chunks:
            chunks.append({
                "text": chunk,
                "page": page_number
            })

    if not chunks:
        raise ValueError("No chunks could be created from the document.")

    return chunks