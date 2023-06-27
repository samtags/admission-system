from flask import Flask, render_template, request, jsonify, redirect, url_for, json
import os
from data import *


app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/register', methods=['post'])
def handle_register():
    data = register_student(dict(request.form))
    return redirect(url_for("admission_reference", id=data['id']))


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/admission-reference/<int:id>')
def admission_reference(id):
    data = get_admission(id)
    return render_template('adrefscreen.html', admissions=data)


@app.route('/adrefscreen')
def display_admissions():
    admissions = get_admissions()
    return render_template('adrefscreen.html', admissions=admissions)


subjects = ["LIS51", "LIS55", "LIS161"]


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


@app.route('/masterlist', methods=['GET', 'POST'])
def master():
    enrolled = get_admissions_by_status("enrolled")

    if request.method == 'POST':
        name = request.form['name']
        subject = request.form['subject']
        results = mastersearch_by_name_and_subject(name, subject)
        return render_template('resultsadref.html', results=results)

    rows_dict = [dict(row) for row in enrolled]

    return render_template('masterlist.html', subjects=subjects, enrolled=rows_dict)


@app.route('/admission/update/<int:id>', methods=['PATCH'])
def update(id):
    data = request.get_json()
    update_admission_status(id, data['status'])
    updated = get_admission(id)
    return jsonify(dict(updated))


@app.route('/accounting', methods=['GET', 'POST'])
def accounting():
    data = {}
    not_found = False

    if request.method == 'POST':
        reference = request.form['reference']
        data = get_admission(reference)

    if (data is None):
        data = {}
        not_found = True

    return render_template('accounting.html', data=data, not_found=not_found)


@app.route('/payment-received/<int:id>', methods=['POST'])
def payment_received(id):
    update_admission_status(id, 'enrolled')
    return redirect(url_for("accounting", success=True))


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
