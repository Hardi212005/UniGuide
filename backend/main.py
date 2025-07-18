from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routes import upload,query

app = FastAPI()

# Enable CORS so frontend (Streamlit) can call backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register upload route
app.include_router(upload.router)
app.include_router(query.router)