from pydantic import BaseModel

class DocumentCreate(BaseModel):
    title:str

class DocumentVersionCreate(BaseModel):
    content:str