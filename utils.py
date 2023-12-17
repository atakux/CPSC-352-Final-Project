import re
import sqlite3

def valid_email(email: str):
  """Check if email str valid"""
  return bool(re.search(r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$", email))

def db_connection(db_path: str) -> sqlite3.Connection:
    """Create DB connection using path str"""
    conn = sqlite3.connect(db_path)
    return conn