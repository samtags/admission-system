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

def readadrefdata(studid):
    conn, cur = connect_db(db_path)
    query = 'SELECT * FROM registrations WHERE id=?'
    results = cur.execute(query, (studid,)).fetchall()
    conn.close()
    return results

def search_by_name_and_subject(name, subject):
    conn, cur = connect_db(db_path)
    query = "SELECT * FROM registrations WHERE name = ? AND subject = ? AND status='pending'"
    cur.execute(query, (name, subject))
    results = cur.fetchall()
    cur.close()
    conn.close()
    return results

def mastersearch_by_name_and_subject(name, subject):
    conn, cur = connect_db(db_path)
    query = "SELECT * FROM registrations WHERE name = ? AND subject = ?"
    cur.execute(query, (name, subject))
    results = cur.fetchall()
    cur.close()
    conn.close()
    return results