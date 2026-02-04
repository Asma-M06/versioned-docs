from uuid import uuid4
from app.db import get_connection


def create_document(title: str):
    conn = get_connection()
    cur = conn.cursor()
    doc_id = str(uuid4())
    cur.execute(
        """
        INSERT INTO documents (id,title) VALUES (%s,%s)
        """ , (doc_id,title),
    )
    conn.commit()
    cur.close()
    conn.close()

    return {"id": doc_id, "title": title}

def create_document_version(document_id : str , content:str):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT COALESCE(MAX(version_number),0) 
        FROM document_versions
        WHERE document_id = %s
        """,(document_id,),
    )
    current_version = cur.fetchone()[0]
    next_version = current_version + 1

    version_id = str(uuid4())

    cur.execute(
        """
        INSERT INTO document_versions (id,document_id,version_number,content) 
        VALUES (%s,%s,%s,%s)
        """,(version_id,document_id,next_version,content),
    )
    conn.commit()
    cur.close()
    conn.close()
    return {"id": version_id, "document_id": document_id, "version_number": next_version, "content": content}

def get_latest_version(document_id:str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT id,version_number,content
        FROM document_versions
        WHERE document_id = %s
        ORDER BY version_number DESC
        LIMIT 1
        """,(document_id,),
    )
    row = cur.fetchone()
    cur.close()
    conn.close()
    if row:
        return {"version_number": row[1], "content": row[2]}
    else:
        return None
    
def get_all_versions(document_id:str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT id,version_number,content
        FROM document_versions
        WHERE document_id = %s
        ORDER BY version_number ASC
        """,(document_id,),
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [
        {
            "version_number":row[0],
            "content":row[1],
            "created_at":row[2]
        }
        for row in rows
    ]

def get_specific_version(document_id:str,version_number:int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT version_number,content,created_at
        FROM document_versions
        WHERE document_id = %s AND version_number = %s
        """,(document_id,version_number),
    )

    row = cur.fetchone()
    cur.close()
    conn.close()

    if row is None:
        return None
    
    return {
        "version_number": row[0],
        "content": row[1],        
        "created_at": row[2]
    }