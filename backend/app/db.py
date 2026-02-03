import psycopg2
import os

def get_connection():
    return psycopg2.connect(
        dbname = os.getenv("DB_NAME","versioned_docs"),
        user = os.getenv("DB_USER","postgres"),
        password = os.getenv("DB_PASSWORD","password"),
        host = os.getenv("DB_HOST","localhost"),
        port = os.getenv("DB_PORT","5432")
    )