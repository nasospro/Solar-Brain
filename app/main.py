from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database path (relative to the file location)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
DB_PATH = os.path.join(PROJECT_ROOT, 'data', 'solar_brain.db')

@app.get("/")
def read_root():
    return {"message": "SolarBrain API is running"}

# This is the decorator you asked for
@app.get("/data")
def get_all_recent_data():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # This converts rows into dictionaries
    cursor = conn.cursor()
    
    # Fetch the last 50 records to have enough data for a chart
    cursor.execute("SELECT * FROM measurements ORDER BY id DESC LIMIT 60")
    rows = cursor.fetchall()
    conn.close()
    
    # Convert list of sqlite3.Row to list of dicts
    data = [dict(row) for row in rows]
    return data

@app.get("/latest")
def get_single_latest_entry():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM measurements ORDER BY id DESC LIMIT 1")
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return dict(row)
    return {"error": "No records found"}