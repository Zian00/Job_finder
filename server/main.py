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


@app.route('/jobs')
def index():
    conn = sqlite3.connect('jobs.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM jobs')
    rv = [dict((cur.description[i][0], value)
               for i, value in enumerate(row)) for row in cur.fetchall()]
    conn.close()
    # print(rv)
    return rv


if __name__ == '__main__':
    create_database()
    app.run(debug=True, port=8080)
