from langchain.vectorstores import Chroma
from langchain.embeddings import OllamaEmbeddings

def get_retriever(db_path, category=None):
    embedding = OllamaEmbeddings(model="nomic-embed-text")
    
    # Load the vector store
    db = Chroma(persist_directory=db_path, embedding_function=embedding)
    
    # Apply metadata filtering if category is selected
    if category:
        retriever = db.as_retriever(
            search_kwargs={
                "k": 10,
                "filter": {
                    "category": category
                }
            }
        )
    else:
        # No filtering
        retriever = db.as_retriever(search_kwargs={"k": 10})

    return retriever
