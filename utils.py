import re
import sqlite3

def valid_email(email: str):
  return bool(re.search(r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$", email))

def db_connection(db_path: str) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    return conn