import os
import sys
import re
import sqlite3
import yagmail

from dotenv import load_dotenv


def valid_email(email: str):
  """Check if email str valid"""
  return bool(re.search(r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$", email))

def db_connection(db_path: str) -> sqlite3.Connection:
  """Create DB connection using path str"""
  conn = sqlite3.connect(db_path)
  return conn

def view_inventory(DB_PATH):
    """Displays the bakery's inventory from inventory.db"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Bakery352")
    rows = cursor.fetchall()
    conn.close()
    return rows

def place_order(username: str, item: str, DB_PATH):
  """Sends email to user with a confirmation of the item they ordered"""

  # retrieve user email from their username
  try:
    conn = db_connection(db_path=DB_PATH)

    # Get user record by username
    cursor = conn.cursor()
    sql = "select * from users where username = ?;"
    cursor.execute(sql, (username,))
    record = cursor.fetchone()

    email = record[2]

    print(f"\nSending email to {username} at email: {email}")
    
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

  except Exception as e:
    print(str(e))
    print("Closing program...")

