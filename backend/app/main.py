from fastapi import FastAPI
from app.db import get_connection
from app.schemas import DocumentCreate
from app.schemas import DocumentVersionCreate
from app.crud import create_document
from app.crud import create_document_version
from app.crud import get_latest_version
from app.crud import get_all_versions
from app.crud import get_specific_version
from app.crud import get_version_content,diff_versions

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

@app.post("/documents/{document_id}/versions")
def add_version(document_id: str, version: DocumentVersionCreate):
    return create_document_version(document_id, version.content)

@app.get("/documents/{document_id}/latest-version")
def get_latest(document_id:str):
    result =  get_latest_version(document_id)
    if result is None :
        return {"error": "No versions found for this document."}
    return result

@app.get("/documents/{document_id}/versions")
def list_versions(document_id:str):
    version =  get_all_versions(document_id)

    if not version :
        return {"error": "No versions found for this document."}
    return version

@app.get("/documents/{document_id}/versions/{version_number}")
def get_version(document_id:str, version_number:int):
    result =  get_specific_version(document_id,version_number)
    if result is None :
        return {"error": "Version not found."}
    return result

@app.get("/documents/{document_id}/diff")
def diff_document_version(
    document_id:str,
    from_version:int,
    to_version:int
):
    content_a = get_version_content(document_id, from_version)
    content_b = get_version_content(document_id, to_version)

    if content_a is None or content_b is None:
        return {"error": "One or both versions not found."}

    diff =  diff_versions(content_a, content_b)

    return {
        "document_id": document_id,
        "from_version": from_version,
        "to_version": to_version,
        "diff": diff
    }