from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse

from backend.utils.croma_db import get_retriever
from backend.config import CHROMA_DB_PATH
from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA

router = APIRouter()

@router.get("/query/")
async def query_answer(question: str = Query(...), category: str = Query(None)):
    """
    Given a question and optional category, return answer using RAG.
    """
    try:
        # 1. Load retriever
        retriever = get_retriever(CHROMA_DB_PATH, category)

        # 2. Load Ollama LLM (Make sure Ollama is running)
        llm = Ollama(model="llama3.2:3b")  # Or whatever model you have loaded

        # 3. RetrievalQA chain
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            retriever=retriever,
            return_source_documents=True
        )

        # 4. Run the chain
        result = qa_chain.invoke({"query": question})
        answer = result["result"]
        sources = [
            {
                "source": doc.metadata.get("source"),
                "category": doc.metadata.get("category"),
                "snippet": doc.page_content[:200]
            }
            for doc in result["source_documents"]
        ]

        return JSONResponse(content={"answer": answer, "sources": sources})

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
