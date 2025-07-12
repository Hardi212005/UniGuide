from langchain_community.embeddings import OllamaEmbeddings
from langchain_ollama import ChatOllama
from langchain.prompts import PromptTemplate, ChatPromptTemplate
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_community.vectorstores import Chroma

from backend.config import CHROMA_DB_PATH

def create_retriever(category: str = None):
    """
    Creates a category-aware MultiQueryRetriever using Ollama LLM and ChromaDB.
    """
    # Embedding and LLM
    embedding = OllamaEmbeddings(model="nomic-embed-text")
    llm = ChatOllama(model="llama3.2:3b")

    # Load Chroma vectorstore
    vectordb = Chroma(
        persist_directory=CHROMA_DB_PATH,
        embedding_function=embedding
    )

    # Rephrasing prompt
    query_prompt = PromptTemplate(
        input_variables=["question"],
        template="""You are an AI assistant. Generate five different rephrased versions of the question below to help retrieve relevant documents from a vector database.

Question: {question}"""
    )

    base_retriever = vectordb.as_retriever(
        search_kwargs={
            "k": 4,
            **({"filter": {"category": category}} if category else {})
        }
    )

    retriever = MultiQueryRetriever.from_llm(
        retriever=base_retriever,
        llm=llm,
        prompt=query_prompt
    )

    return retriever, llm


def create_chain(retriever, llm):
    """
    Creates a QA chain that strictly answers using only retrieved context.
    """
    prompt_template = """Answer the question using ONLY the following context:
{context}

Question: {question}

Instructions:
- If the context contains relevant information to answer the question, provide a detailed answer using only that information.
- If the context does not contain relevant information to answer the question, respond EXACTLY with: "I'm sorry, I could not find relevant information in the uploaded documents to answer your question."
- Do not use any external knowledge. Only use the provided context.

Answer:"""

    prompt = ChatPromptTemplate.from_template(prompt_template)

    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain
