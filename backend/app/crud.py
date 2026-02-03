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