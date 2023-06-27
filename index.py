from flask import Flask, render_template, request, jsonify, redirect, url_for
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
    if request.method == 'POST':
        name = request.form['name']
        subject = request.form['subject']
        results = search_by_name_and_subject(name, subject)
        return render_template('resultsadstaff.html', results=results)
    return render_template('searchadstaff.html', subjects=subjects)


@app.route('/masterlist', methods=['GET', 'POST'])
def master():
    if request.method == 'POST':
        name = request.form['name']
        subject = request.form['subject']
        results = mastersearch_by_name_and_subject(name, subject)
        return render_template('resultsadref.html', results=results)
    return render_template('searchadref.html', subjects=subjects)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
