import re
import sqlite3

def valid_email(email: str):
  return bool(re.search(r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$", email))

def db_connection(db_path: str) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    return conn


# -----------------------------------------------
# Hashing with Salt imports and methods
from os import urandom
from hashlib import pbkdf2_hmac

def hash_password(password: str):
    salt_val = urandom(16)
    hashed_pw = pbkdf2_hmac('sha256', password.encode(), salt_val, 100000)
    return (salt_val, hashed_pw)

def check_password(password: str, salt_val: bytes, hash: bytes):
    if hash == pbkdf2_hmac('sha256', password.encode(), salt_val, 100000):
        return True
    return False
# -----------------------------------------------
