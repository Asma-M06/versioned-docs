from fastapi import FastAPI
from app.db import get_connection
from app.crud import create_document
from app.schemas import DocumentCreate
app = FastAPI()

@app.get("/")
def health_check():
    return {"status": "ok"}

@app.get("/db-check")
def db_check():
    try:
        conn = get_connection()
        conn.close()
        return {"db": "connected"}
    except Exception as e:
        return {"error": str(e)}

@app.post("/documents/")
def create_doc(doc:DocumentCreate):
    return create_document(doc.title)