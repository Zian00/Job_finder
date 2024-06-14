from flask_cors import CORS
from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3

app = Flask(__name__)
cors = CORS(app, origin='*')

def get_db_connection():
    conn = sqlite3.connect('jobs.db')
    conn.row_factory = sqlite3.Row  # This allows dictionary-like access to rows
    return conn

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


@app.route('/3jobs', methods=['GET'], strict_slashes=False)
def getThreeJobs():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('''SELECT
                            c.name,
                            c.companyDescription,
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
                            join jobs j on j.companyId = c.id
                        LIMIT 3;''')
        data = cur.fetchall()

        data_result = []
        for row in data:
            data_result.append(dict(row))
    except sqlite3.Error as error:
        print("Failed to fetch data from database\n", error)
    finally:
        if conn:
            conn.close()
            print("The SQLite connection is closed")
        return data_result

@app.route('/jobs', methods=['GET'], strict_slashes=False)
def getAllJobs():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('''SELECT
                            c.name,
                            c.companyDescription,
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
            data_result.append(dict(row))
    except sqlite3.Error as error:
        print("Failed to fetch data from database\n", error)
    finally:
        if conn:
            conn.close()
            print("The SQLite connection is closed")
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
    company_description = frontend_inputs["company"]["companyDescription"]
    company_contactEmail = frontend_inputs["company"]["contactEmail"]
    company_contactPhone = frontend_inputs["company"]["contactPhone"]
    try:
        conn = sqlite3.connect('jobs.db')
        cur = conn.cursor()
        cur.execute('INSERT INTO companies (name, companyDescription, contactEmail, contactPhone) VALUES (?, ?, ?, ?)',
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


@app.route('/jobs/<int:id>', methods=['GET'], strict_slashes=False)
def getJobById(id):
    try:
        conn = sqlite3.connect('jobs.db')
        conn.row_factory = sqlite3.Row

        cur = conn.cursor()
        cur.execute('''SELECT
                        c.name,
                        c.companyDescription,
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
                        join jobs j on j.companyId = c.id
                    WHERE 
                        j.id = ? ;''', (id,))
        row = cur.fetchone()

        row_dict = dict(row)
        # print(row_dict)

    except sqlite3.Error as error:
        print("Failed to get job data by id\n", error)
    finally:
        if conn:
            conn.close()
            print("The SQLite connection is closed")
            return row_dict


@app.route('/jobs/<int:id>', methods=['PUT'], strict_slashes=False)
def updateJobById(id):
    frontend_inputs = request.get_json()
    
    title = frontend_inputs["title"]
    job_type = frontend_inputs["type"]
    location = frontend_inputs["location"]
    description = frontend_inputs["description"]
    salary = frontend_inputs["salary"]
    company_name = frontend_inputs["company"]["name"]
    company_description = frontend_inputs["company"]["companyDescription"]
    company_contactEmail = frontend_inputs["company"]["contactEmail"]
    company_contactPhone = frontend_inputs["company"]["contactPhone"]

    try:
        conn = sqlite3.connect('jobs.db')
        cur = conn.cursor()
        cur.execute('''UPDATE companies
                        SET name = ?, companyDescription = ?, ContactEmail = ?, ContactPhone = ?
                        FROM jobs
                        WHERE companies.id = jobs.companyId
                        AND jobs.id = ?;''', (company_name, company_description, company_contactEmail, company_contactPhone, id))
        conn.commit()

        cur.execute('''UPDATE jobs
                        SET title =?, type =?, location =?, description =?, salary =?
                        WHERE id =?;''', (title, job_type, location, description, salary, id))

        conn.commit()

    except sqlite3.Error as error:
        print("Failed to update data\n", error)
    finally:
        if conn:
            conn.close()
        print("The SQLite connection is closed")
        return "Data updated sucessfully"


@app.route('/jobs/<int:id>', methods=['DELETE'], strict_slashes=False)
def deleteJobById(id):
    try:
        conn = sqlite3.connect('jobs.db')
        cur = conn.cursor()
        cur.execute('''DELETE FROM jobs WHERE id =?;''', (id,))
        conn.commit()
    except sqlite3.Error as error:
        print("Failed to delete data\n", error)
    finally:
        if conn:
            conn.close()
        print("The SQLite connection is closed")
        return "Data deleted successfully"
    
if __name__ == '__main__':
    create_database()
    app.run(debug=True, port=8080)
