from langchain_community.document_loaders import UnstructuredPDFLoader
from langchain_core.documents import Document
from typing import List

def load_pdf_as_documents(pdf_path: str, category: str) -> List[Document]:
    """
    Loads a PDF using LangChain's UnstructuredPDFLoader and attaches metadata.

    Returns:
        List[Document]: A list of LangChain Document objects with metadata.
    """
    loader = UnstructuredPDFLoader(pdf_path)
    documents = loader.load()

    file_name = pdf_path.split("/")[-1]

    # Add source, file_name, and category metadata to each document
    for doc in documents:
        doc.metadata["source"] = file_name
        doc.metadata["file_name"] = file_name
        doc.metadata["category"] = category

    return documents
