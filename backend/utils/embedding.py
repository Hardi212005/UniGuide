import os
from langchain_ollama import OllamaEmbeddings 
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from typing import List

from backend.config import CHROMA_DB_PATH

# Initialize embedding model (requires Ollama running with `nomic-embed-text`)
embedding_model = OllamaEmbeddings(model="nomic-embed-text")

# Text splitter to create chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)

def embed_and_store_documents(documents: List[Document]):
    """
    Splits documents into chunks, embeds them using Ollama, and stores in ChromaDB with metadata.

    Args:
        documents (List[Document]): List of LangChain Document objects (with metadata).
    """
    # Split into chunks while retaining metadata
    chunks = text_splitter.split_documents(documents)

    # Load or create persistent vector store
    vectordb = Chroma(
        persist_directory=CHROMA_DB_PATH,
        embedding_function=embedding_model
    )

    vectordb.add_documents(chunks)
    vectordb.persist()
