from flask import Flask, render_template, request
import os
import sqlite3
from data import register_student


db_path = 'records.db'

app = Flask(__name__)

# Connect to a database


def connect_db(path):
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    return (conn, conn.cursor())


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/register', methods=['post'])
def handle_register():

    admission = register_student(request.json)
    return jsonify({
        "id": admission[0],
        "name": admission[1],
        "subject": admission[2],
        "email": admission[3],
        "phone": admission[4],
        "tel": admission[5],
        "dob": admission[6]
    })


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/admissionreference')
def adref():
    return render_template('adrefscreen.html')


@app.route('/adstaffscreen', methods=['GET', 'POST'])
def adstaff():
    # Get the search and filter criteria from the form
    searchdbpending = request.form.get('searchdbpending', '')
    filterbycourse = request.form.get('filterbycourse', '')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # Build the SQL query based on the search and filter criteria
    query = "SELECT * FROM registrations WHERE subject=?"
    params = ('%' + searchdbpending + '%',)
    if filterbycourse:
        query += " AND another_column = ?"
        params += (filterbycourse,)
    # Execute the query and fetch the results
    cursor.execute(query, params)
    results = cursor.fetchall()
    # Close the database connection
    cursor.close()
    conn.close()
    # Pass the results to the HTML template
    return render_template('adstaffscreen.html', results=results)


@app.route('/masterlist', methods=['GET', 'POST'])
def master():
    # Get the search and filter criteria from the form
    mstrsearchdbpending = request.form.get('mstrsearchdbpending', '')
    mstrfilterbycourse = request.form.get('mstrfilterbycourse', '')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # Build the SQL query based on the search and filter criteria
    query = "SELECT * FROM registrations WHERE subject=?"
    params = ('%' + mstrsearchdbpending + '%',)
    if mstrfilterbycourse:
        query += " AND another_column = ?"
        params += (mstrfilterbycourse,)
    # Execute the query and fetch the results
    cursor.execute(query, params)
    results = cursor.fetchall()
    # Close the database connection
    cursor.close()
    conn.close()
    # Pass the results to the HTML template
    return render_template('masterlist.html', results=results)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
