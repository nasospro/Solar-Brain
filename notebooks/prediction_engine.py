import sqlite3
import joblib
import pandas as pd
import time
import os


model = joblib.load('solar_model.pkl')
scaler = joblib.load('scaler.pkl')

def get_latest_data():
    conn = sqlite3.connect('solar_brain.db')
    
    query = "SELECT id, irradiance, temperature, power FROM measurements ORDER BY id DESC LIMIT 1"
                 
    df = pd.read_sql_query(query, conn)               
                
    conn.close()
    return df

while True:
    df_raw = get_latest_data()

    if not df_raw.empty:
        row_id = int(df_raw['id'].values[0]) 
        
        irr = df_raw['irradiance'].values[0]
        temp_base = df_raw['temperature'].values[0]
        actual_power = df_raw['power'].values[0]

        ambient_temp = temp_base
        module_temp = temp_base + 5.0

        X_live = pd.DataFrame([[ambient_temp, module_temp, irr]], 
                             columns=['AMBIENT_TEMPERATURE', 'MODULE_TEMPERATURE', 'IRRADIATION'])

        X_scaled = scaler.transform(X_live)
        prediction = float(model.predict(X_scaled)[0])

        conn = sqlite3.connect('solar_brain.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE measurements SET predicted_power = ? WHERE id = ?", (prediction, row_id))
        conn.commit()
        conn.close()

        error = abs(actual_power - prediction)
        print(f"--- Live Update (Row ID: {row_id}) ---")
        print(f"Actual: {actual_power:.2f}W | Predicted: {prediction:.2f}W")
        print(f"Error: {error:.2f}W")
        print("-" * 20)

    time.sleep(3)


