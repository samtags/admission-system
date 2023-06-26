import sqlite3
from pprint import pprint

db_path = 'records.db'

# Connect to a database


def connect_db(path):
    conn = sqlite3.connect(path)
    # Convert tuples to dictionaries
    conn.row_factory = sqlite3.Row
    return (conn, conn.cursor())


def register_student(payload):
    conn, cur = connect_db(db_path)
    query = 'INSERT INTO registrations (name, subject, email, phone, tel, dob) VALUES (?,?,?,?,?,?)'
    values = (payload['name'],
              payload['subject'],
              payload['email'],
              payload['phone'],
              payload['tel'],
              payload['dob'])
    cur.execute(query, values)

    select = 'SELECT * FROM registrations WHERE id=?'
    values = (cur.lastrowid,)
    row = cur.execute(select, values).fetchone()

    conn.commit()
    conn.close()
    return row
