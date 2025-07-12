# UniGuide
# 🎓 UniGuide – College Query Assistant

UniGuide is an intelligent assistant built to help **students, professors, and administrators** navigate college-related queries using document-based Q&A powered by LLMs. It leverages advanced retrieval-augmented generation (RAG) to fetch accurate answers strictly from uploaded institutional documents.

---

## 🚀 Features

- 🔍 **Ask Queries Across PDFs**  
  Students can ask questions and receive precise answers extracted from relevant college documents.

- 🧑‍🏫 **Role-Based Access Control**  
  - **Professors & Admins** can upload new documents and ask questions.  
  - **Students** can only ask questions.

- 🗂️ **Document Categorization**  
  Upload PDFs under specific categories like `course`, `degree`, `announcements`, `professor_details`, and `facilities`.

- 🧠 **LLM-powered Retrieval**  
  Uses LangChain + Ollama + ChromaDB to enable smart document chunking, embedding, multi-query retrieval, and strict answer generation.

- ♻️ **Persistent Embeddings**  
  Embeddings and uploaded files are stored persistently — no reprocessing needed on restart.

---




