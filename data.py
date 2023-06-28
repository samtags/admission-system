import sqlite3
from utils import generate_random_hash

db_path = 'records.db'

# Connect to a database


def connect_db(path):
    conn = sqlite3.connect(path)
    # Convert tuples to dictionaries
    conn.row_factory = sqlite3.Row
    return (conn, conn.cursor())

# Insert new registration into the database


def register_student(payload):
    conn, cur = connect_db(db_path)
    # query = 'INSERT INTO registrations (name, subject, email, phone, dob, status) VALUES (?,?,?,?,?,?)'
    query = 'INSERT INTO registrations (first_name, middle_name, last_name, dob, sex, address, email, phone, status, reference, emergency_contact_name, emergency_contact_number, emergency_contact_relation) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)'

    default_status = "pending"
    reference = generate_random_hash(5)

    values = (payload['first_name'],
              payload['middle_name'],
              payload['last_name'],
              payload['dob'],
              payload['sex'],
              payload['address'],
              payload['email'],
              payload['phone'],
              default_status,
              reference,
              payload['emergency_contact_name'],
              payload['emergency_contact_number'],
              payload['emergency_contact_relation']
              )
    cur.execute(query, values)
    # Selects newly inserted row
    select = 'SELECT * FROM registrations WHERE id=?'
    values = (cur.lastrowid,)
    row = cur.execute(select, values).fetchone()
    conn.commit()
    conn.close()
    return row

# Retreives data based on id


def get_admission(id):
    conn, cur = connect_db(db_path)
    query = 'SELECT * FROM registrations WHERE id=?'
    values = (id,)
    row = cur.execute(query, values).fetchone()
    conn.close()
    return row


def get_admission_by_reference(reference):
    conn, cur = connect_db(db_path)
    query = 'SELECT * FROM registrations WHERE reference=?'
    values = (reference,)
    row = cur.execute(query, values).fetchone()
    conn.close()
    return row


# Removes registration from database
def remove_admission(id):
    conn, cur = connect_db(db_path)
    query = 'DELETE FROM registrations WHERE id=?'
    values = (id,)
    cur.execute(query, values)
    conn.commit()
    conn.close()
    return True

# Selects all registrations from the database


def get_all_admissions():
    conn, cur = connect_db(db_path)
    query = 'SELECT * FROM registrations'
    row = cur.execute(query).fetchall()
    conn.close()
    return row

# Retrieves all registrations that have a specific status


def get_admissions_by_status(status):
    conn, cur = connect_db(db_path)
    query = 'SELECT * FROM registrations WHERE status=?'
    values = (status,)
    row = cur.execute(query, values).fetchall()
    conn.close()
    return row

# Updates the status of a registration


def update_admission_status(id, status):
    conn, cur = connect_db(db_path)
    query = 'UPDATE registrations SET status=? WHERE id=?'
    values = (status, id)
    cur.execute(query, values)
    conn.commit()
    conn.close()
    return True

# Retrieves registrations that have a specific name, subject, or status


def get_admissions():
    conn, cur = connect_db(db_path)
    cur.execute('SELECT name, subject, status FROM registrations')
    admissions = cur.fetchall()
    conn.close()
    return admissions

# Searches the database for pending registrations with a specific name and subject and returns all registrations that match


def search_by_name_and_subject(name, subject):
    conn, cur = connect_db(db_path)
    query = "SELECT * FROM registrations WHERE name = ? AND subject = ? AND status='pending'"
    cur.execute(query, (name, subject))
    results = cur.fetchall()
    cur.close()
    conn.close()
    return results

# searches the database with a specific name and subject, and returns all registrations that match


def mastersearch_by_name_and_subject(name, subject):
    conn, cur = connect_db(db_path)
    query = "SELECT * FROM registrations WHERE name = ? AND subject = ?"
    cur.execute(query, (name, subject))
    results = cur.fetchall()
    cur.close()
    conn.close()
    return results
