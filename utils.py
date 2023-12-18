import os
import re
import sqlite3
import yagmail
from pathlib import Path

from dotenv import load_dotenv
from Crypto.PublicKey import RSA

# Added for view_inventory() to access the bakery's inventory list
DB = "secure_purchase_order.db"
PARENT_DIR = Path.cwd().parent
DB_PATH = PARENT_DIR/DB

def valid_email(email: str):
  """Check if email str valid"""
  return bool(re.search(r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$", email))

def db_connection(db_path: str) -> sqlite3.Connection:
  """Create DB connection using path str"""
  conn = sqlite3.connect(db_path)
  return conn

def view_inventory():
    """Displays the bakery's inventory from inventory.db"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Bakery352")
    rows = cursor.fetchall()
    conn.close()
    return rows

def place_order(username: str, email: str, item: str):
  """Sends email to user with a confirmation of the item they ordered"""

  load_dotenv()

  mgr_email = os.environ['EMAIL']
  mgr_password = os.environ['PASSWORD']

  yag = yagmail.SMTP(mgr_email, mgr_password)

  contents = [
              f"Hello {username}!",
              f"\nYou ordered {item}.",
              "\n\nThank you!"
  ]

  yag.send(email, 'Order Confirmation', contents)

