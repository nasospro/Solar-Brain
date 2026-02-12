from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import joblib
import os
import pandas as pd

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
DB_PATH = os.path.join(PROJECT_ROOT, 'data', 'solar_brain.db')

MODEL_PATH = os.path.join(PROJECT_ROOT, 'models', 'solar_model.pkl')
SCALER_PATH = os.path.join(PROJECT_ROOT, 'models', 'scaler.pkl')

model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)

@app.get("/")
def read_root():
    return {"message": "SolarBrain API is running"}

@app.get("/data")
def get_all_recent_data():
    conn = sqlite3.connect(DB_PATH, timeout=10)
    conn.row_factory = sqlite3.Row 
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, timestamp, irradiance, temperature, power FROM measurements ORDER BY id DESC LIMIT 60")
    rows = cursor.fetchall()
    
    
    if not rows:
        conn.close()
        return []

    df = pd.DataFrame([dict(r) for r in rows])
    
    X_batch = pd.DataFrame({
        'AMBIENT_TEMPERATURE': df['temperature'],
        'MODULE_TEMPERATURE': df['temperature'] + 5.0,
        'IRRADIATION': df['irradiance']
    })
    
    X_scaled = scaler.transform(X_batch)
    predictions = model.predict(X_scaled)
    
    df['api_predicted_power'] = predictions.round(2)

    update_tuples = [(row['api_predicted_power'], row['id']) for _, row in df.iterrows()]
    cursor.executemany("UPDATE measurements SET predicted_power = ? WHERE id = ?", update_tuples)
    
    conn.commit()
    conn.close()
    
    return df.to_dict(orient='records')

@app.get("/latest")
def get_single_latest_entry():
    conn = sqlite3.connect(DB_PATH, timeout=10)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, irradiance, temperature, power FROM measurements ORDER BY id DESC LIMIT 1")
    row = cursor.fetchone()
    
    if not row:
            conn.close()
            return {"error": "No data found"}
    
    d = dict(row)
    row_id = d['id']
    temp_base = d['temperature']
    irr = d['irradiance']
    actual_p = d['power']

        
    X_live = pd.DataFrame(
        [[temp_base, temp_base + 5.0, irr]], 
         columns=['AMBIENT_TEMPERATURE', 'MODULE_TEMPERATURE', 'IRRADIATION']
        )
        
    X_scaled = scaler.transform(X_live)
    prediction = float(model.predict(X_scaled)[0])
    rounded_pred = round(prediction, 2)
        
    d['api_predicted_power'] = rounded_pred

    cursor.execute("UPDATE measurements SET predicted_power = ? WHERE id = ?", (rounded_pred, row_id))
    conn.commit()
    conn.close()
        
    if actual_p < (prediction * 0.8):
                d['status'] = "⚠️ Alert: Low Efficiency Detected"
                d['is_alert'] = True
    else:
                d['status'] = "✅ Healthy"
                d['is_alert'] = False

    return d

@app.post("/predict")
async def predict_manual(temp: float = Form(...), irr: float = Form(...)):
    X_manual = pd.DataFrame(
        [[temp, temp + 5.0, irr]], 
        columns=['AMBIENT_TEMPERATURE', 'MODULE_TEMPERATURE', 'IRRADIATION']
    )
    
    X_scaled = scaler.transform(X_manual)
    prediction = float(model.predict(X_scaled)[0])
    
    return {
        "predicted_power": round(prediction, 2),
        "message": f"In a scenario with {temp}°C and {irr} W/m², the system would produce {prediction:.2f}W"
    }