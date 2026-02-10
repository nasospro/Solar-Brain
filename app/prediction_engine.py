import sqlite3
import joblib
import pandas as pd
import time
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
DB_PATH = os.path.join(PROJECT_ROOT, 'data', 'solar_brain.db')
MODEL_PATH = os.path.join(PROJECT_ROOT, 'models', 'solar_model.pkl')
SCALER_PATH = os.path.join(PROJECT_ROOT, 'models', 'scaler.pkl')

model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)

def get_latest_data(DB_PATH):
    conn = sqlite3.connect(DB_PATH)
    query = "SELECT id, irradiance, temperature, power FROM measurements WHERE predicted_power IS NULL ORDER BY id DESC LIMIT 1"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

while True:
    # Use the dynamic db_path variable
    df_raw = get_latest_data(DB_PATH)

    if not df_raw.empty:
        row_id = int(df_raw['id'].values[0]) 
        irr = df_raw['irradiance'].values[0]
        temp_base = df_raw['temperature'].values[0]
        actual_power = df_raw['power'].values[0]

        # Prepare features for the AI model
        ambient_temp = temp_base
        module_temp = temp_base + 5.0

        X_live = pd.DataFrame([[ambient_temp, module_temp, irr]], 
                             columns=['AMBIENT_TEMPERATURE', 'MODULE_TEMPERATURE', 'IRRADIATION'])

        # Predict
        X_scaled = scaler.transform(X_live)
        prediction = float(model.predict(X_scaled)[0])

        # Update the database using DB_PATH
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("UPDATE measurements SET predicted_power = ? WHERE id = ?", (prediction, row_id))
        conn.commit()
        conn.close()

        error = abs(actual_power - prediction)
        print(f"--- Live Update (Row ID: {row_id}) ---")
        print(f"Actual: {actual_power:.2f}W | Predicted: {prediction:.2f}W")
        print(f"Error: {error:.2f}W")
        print("-" * 20)
    else:
        print("Waiting for new data from simulation...")

    time.sleep(3)


