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
    query = 'INSERT INTO registrations (name, subject, email, phone, dob, status) VALUES (?,?,?,?,?,?)'
    values = (payload['name'],
              payload['subject'],
              payload['email'],
              payload['phone'],
              payload['dob'],
              "pending"
              )
    cur.execute(query, values)

    select = 'SELECT * FROM registrations WHERE id=?'
    values = (cur.lastrowid,)
    row = cur.execute(select, values).fetchone()

    conn.commit()
    conn.close()
    return row


def get_admission(id):
    conn, cur = connect_db(db_path)
    query = 'SELECT * FROM registrations WHERE id=?'
    values = (id,)
    row = cur.execute(query, values).fetchone()
    conn.close()
    return row


def get_admissions_by_status(status):
    conn, cur = connect_db(db_path)
    query = 'SELECT * FROM registrations WHERE status=?'
    values = (status,)
    row = cur.execute(query, values).fetchall()
    conn.close()
    return row


def update_admission_status(id, status):
    conn, cur = connect_db(db_path)
    query = 'UPDATE registrations SET status=? WHERE id=?'
    values = (status, id)
    cur.execute(query, values)
    conn.commit()
    conn.close()
    return True


def get_admissions():
    conn, cur = connect_db(db_path)
    cur.execute('SELECT name, subject, status FROM registrations')
    admissions = cur.fetchall()
    conn.close()
    return admissions


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
