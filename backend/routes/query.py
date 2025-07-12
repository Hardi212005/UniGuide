from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse

from backend.utils.croma_db import create_retriever, create_chain

router = APIRouter()

@router.get("/query/")
async def query_answer(question: str = Query(...), category: str = Query(None)):
    """
    Answer a question strictly using uploaded documents (category-specific if provided).
    If relevant context is not found, responds with a default fallback message.
    """
    try:
        # Step 1: Create retriever and LLM
        retriever, llm = create_retriever(category)

        # Step 2: Create strict RAG chain
        chain = create_chain(retriever, llm)

        # Step 3: Run the chain with user's question
        answer = chain.invoke(question)

        return JSONResponse(content={"answer": answer})

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
