from flask import Flask, render_template, request, jsonify, redirect, url_for, json
import os
from data import *
from flask_socketio import SocketIO

app = Flask(__name__)
# Added socketio to enable realtime communication between server and client
socketio = SocketIO(app)

# Broadcasts admission data to clients through socketio


def broadcast(table: str, id=None, **kwargs):
    if (id):
        updated = get_admission(id)
        if (updated):
            socketio.emit(f"registrations/{id}", {'data': dict(updated)})

    if (kwargs.get("all")):
        admissions = get_all_admissions()
        rows_dict = [dict(row) for row in admissions]
        socketio.emit('registrations', {'data': rows_dict})
        return

    if (table == "registrations"):
        pending_admissions = get_admissions_by_status("pending")
        rows_dict = [dict(row) for row in pending_admissions]
        socketio.emit('registrations', {'data': rows_dict})

# Homepage


@app.route('/')
def home():
    return render_template('index.html')

# Register page. Handles registration of students


@app.route('/register', methods=['post'])
def handle_register():
    # Retrieves form data from the request and converts it to a dictionary
    data = register_student(dict(request.form))
    # Broadcast data to clients using socketio
    broadcast("registrations")
    return redirect(url_for("admission_reference", id=data['id']))


@app.route('/register')
def register():
    return render_template('register.html')

# Calls get_admission function in data.py and passes the id of the registration to the template


@app.route('/admission-reference/<int:id>')
def admission_reference(id):
    data = get_admission(id)
    return render_template('adrefscreen.html', admissions=data, id=id)


@app.route('/adrefscreen')
def display_admissions():
    admissions = get_admissions()
    return render_template('adrefscreen.html', admissions=admissions)


subjects = ["LIS51", "LIS55", "LIS161"]

# Retrieves PENDING registrations in the database and passes them to the template


@app.route('/search', methods=['GET', 'POST'])
def search():
    pending_admissions = get_admissions_by_status("pending")
    if request.method == 'POST':
        name = request.form['name']
        subject = request.form['subject']
        results = search_by_name_and_subject(name, subject)
        return render_template('resultsadstaff.html', results=results)
    rows_dict = [dict(row) for row in pending_admissions]
    return render_template('searchadstaff.html', subjects=subjects, admissions=rows_dict)

# Retrieves ALL registrationsin the database and passes them to the template


@app.route('/masterlist', methods=['GET', 'POST'])
def master():
    admissions = get_all_admissions()

    if request.method == 'POST':
        name = request.form['name']
        subject = request.form['subject']
        results = mastersearch_by_name_and_subject(name, subject)
        return render_template('resultsadref.html', results=results)

    rows_dict = [dict(row) for row in admissions]

    return render_template('masterlist.html', subjects=subjects, admissions=rows_dict)

# Accepts or Rejects a registration


@app.route('/registrations/<int:id>', methods=['PATCH', "DELETE"])
def registrations(id):
    # Updates the database if ccepted
    if (request.method == "PATCH"):
        data = request.get_json()
        update_admission_status(id, data['status'])
        broadcast("registrations", id)
        updated = get_admission(id)
        return jsonify(dict(updated))
    # Deletes the registration from the database if Rejected
    if (request.method == "DELETE"):
        remove_admission(id)
        broadcast("registrations", all=True)
        return jsonify({"message": "success"})
    # For neither accept nor reject
    return "Not found."

# Searches for a registration by admission reference number


@app.route('/accounting', methods=['GET', 'POST'])
def accounting():
    data = {}
    not_found = False
    # Retrieves admission data from the database
    if request.method == 'POST':
        reference = request.form['reference']
        data = get_admission_by_reference(reference)
    # Handles the case where no data is found
    if (data is None):
        data = {}
        not_found = True
    return render_template('accounting.html', data=data, not_found=not_found)

# Updates the status of a registration once payment is received


@app.route('/payment-received/<int:id>', methods=['POST'])
def payment_received(id):
    update_admission_status(id, 'enrolled')
    broadcast("registrations", id)
    return redirect(url_for("accounting", success=True))


@app.route('/staff')
def staffdirectory():
    return render_template('staff.html')


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
