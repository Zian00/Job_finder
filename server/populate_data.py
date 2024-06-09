import json
import sqlite3

# Load JSON data
with open('../client/src/jobs.json') as f:
    data = json.load(f)

# Connect to SQLite database
conn = sqlite3.connect('jobs.db')
cursor = conn.cursor()

# Create tables
cursor.execute('''
CREATE TABLE IF NOT EXISTS companies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    companyDescription TEXT NOT NULL,
    contactEmail TEXT NOT NULL,
    contactPhone TEXT NOT NULL
)''')

cursor.execute('''
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

# Insert data into tables
for job in data['jobs']:
    # Insert company data and get company id
    company = job['company']
    cursor.execute('''
    INSERT INTO companies (name, companyDescription, contactEmail, contactPhone)
    VALUES (?, ?, ?, ?)''', (company['name'], company['description'], company['contactEmail'], company['contactPhone']))
    
    company_id = cursor.lastrowid
    
    # Insert job data
    cursor.execute('''
    INSERT INTO jobs (title, type, location, description, salary, companyId)
    VALUES (?, ?, ?, ?, ?, ?)''', (job['title'], job['type'], job['location'], job['description'], job['salary'], company_id))

# Commit changes and close connection
conn.commit()
conn.close()
