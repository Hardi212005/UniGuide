from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
import os

from backend.config import CHROMA_DB_PATH

# Initialize embedding model
embedding_model = OllamaEmbeddings(model="nomic-embed-text")  # Ensure ollama is running

# Split long text into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)

def store_pdf_text(text: str, file_name: str, category: str, metadata: dict = None):
    """
    Splits PDF text, generates embeddings using Ollama, and stores in ChromaDB with metadata.
    """
    chunks = text_splitter.split_text(text)

    # Base metadata: always include source (file name) and category
    base_metadata = {
        "source": file_name,
        "file_name": file_name,
        "category": category
    }

    # Merge extra metadata if provided
    if metadata:
        base_metadata.update(metadata)

    documents = [
        Document(
            page_content=chunk,
            metadata=base_metadata.copy()  # Avoid mutation across chunks
        )
        for chunk in chunks
    ]

    # Load or create persistent ChromaDB
    vectordb = Chroma(
        persist_directory=CHROMA_DB_PATH,
        embedding_function=embedding_model
    )

    vectordb.add_documents(documents)
    vectordb.persist()
