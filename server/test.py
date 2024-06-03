import json
import sqlite3

# Load JSON data
with open('../client/src/jobs.json') as f:
    data = json.load(f)
    print(data)