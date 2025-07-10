import os

# Get the absolute path to the backend folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Join it with data/chroma_db
CHROMA_DB_PATH = os.path.join(BASE_DIR, "data", "chroma_db")
