from flask_cors import CORS
from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3

app = Flask(__name__)
cors = CORS(app, origin='*')


def create_database():
    conn = sqlite3.connect('jobs.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS jobs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        type TEXT NOT NULL,
        location TEXT NOT NULL,
        description TEXT NOT NULL,
        salary TEXT NOT NULL,
        companyId INTEGER,
        FOREIGN KEY (companyId) REFERENCES companies (id)
    );''')

    c.execute('''
    CREATE TABLE IF NOT EXISTS jobs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        type TEXT NOT NULL,
        location TEXT NOT NULL,
        description TEXT NOT NULL,
        salary TEXT NOT NULL,
        companyId INTEGER,
        FOREIGN KEY (companyId) REFERENCES companies (id)
    )''')
    conn.commit()
    conn.close()


@app.route('/')
def index():
    return "API is working"


@app.route('/jobs', methods=['GET'], strict_slashes=False)
def getAllJobs():
    conn = sqlite3.connect('jobs.db')
    cur = conn.cursor()
    cur.execute('''SELECT
                        c.name,
                        c.description,
                        c.contactEmail,
                        c.contactPhone,
                        j.id,
                        j.title,
                        j.type,
                        j.location,
                        j.description,
                        j.salary
                    FROM
                        companies c
                        join jobs j on j.companyId = c.id;''')

    data = cur.fetchall()
    data_result = []

    for row in data:
        row_dict = {}
        for i, value in enumerate(row):
            column_name = cur.description[i][0]
            row_dict[column_name] = value
        data_result.append(row_dict)
    # print(data_result)

    conn.close()

    return data_result


@app.route('/jobs', methods=['POST'], strict_slashes=False)
def addJob():

    frontend_inputs = request.get_json()

    title = frontend_inputs["title"]
    job_type = frontend_inputs["type"]
    location = frontend_inputs["location"]
    description = frontend_inputs["description"]
    salary = frontend_inputs["salary"]
    company_name = frontend_inputs["company"]["name"]
    company_description = frontend_inputs["company"]["description"]
    company_contactEmail = frontend_inputs["company"]["contactEmail"]
    company_contactPhone = frontend_inputs["company"]["contactPhone"]
    try:
        conn = sqlite3.connect('jobs.db')
        cur = conn.cursor()
        cur.execute('INSERT INTO companies (name, description, contactEmail, contactPhone) VALUES (?, ?, ?, ?)',
                    (company_name, company_description, company_contactEmail, company_contactPhone))
        conn.commit()
        cur.execute("SELECT id FROM companies WHERE name = ?",
                    (company_name,))

        # get the id of company table for setting foreign key in jobs table
        data = cur.fetchone()
        id_of_new_data = data[0]

        cur.execute(
            'INSERT INTO jobs (title, type, location, description, salary, companyId) VALUES (?, ?, ?, ?, ?, ?)',
            (title, job_type, location, description, salary, id_of_new_data))
        conn.commit()

    except sqlite3.Error as error:
        print("Failed to insert data\n", error)
    finally:
        if conn:
            conn.close()
        print("The SQLite connection is closed")
        return "New data recorded"


if __name__ == '__main__':
    create_database()
    app.run(debug=True, port=8080)
