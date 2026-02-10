import streamlit as st
import sqlite3
import pandas as pd
import plotly.graph_objects as go
import time
import os

st.set_page_config(page_title="SolarBrain AI Monitor", layout="wide")

def get_data():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    PROJECT_ROOT = os.path.dirname(BASE_DIR)
    DB_PATH = os.path.join(PROJECT_ROOT, 'data', 'solar_brain.db')
    
    try:  
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query("SELECT * FROM measurements ORDER BY id DESC LIMIT 60", conn)
        conn.close()
        return df.sort_values('id')
    except Exception as e:
        st.error(f"Database connection error: {e}")
        return pd.DataFrame()

st.title("☀️ SolarBrain Live: AI Prediction Analysis")
st.markdown("---")

placeholder = st.empty()

while True:
    df = get_data()
    
    if not df.empty:
        with placeholder.container():
            latest = df.iloc[-1]
            actual = latest['power']
            pred = latest['predicted_power'] if latest['predicted_power'] is not None else 0
            error = abs(actual - pred)
            
            m1, m2, m3 = st.columns(3)
            m1.metric("Actual Power", f"{actual:.2f} W")
            m2.metric("AI Prediction", f"{pred:.2f} W")
            
            error_p = (error / actual * 100) if actual > 0 else 0
            m3.metric("Error", f"{error:.2f} W", delta=f"{error_p:.1f}%", delta_color="inverse")

            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=df['id'], y=df['power'], 
                name="Actual Power", 
                line=dict(color='#FFA500', width=4)
            ))
            
            fig.add_trace(go.Scatter(
                x=df['id'], y=df['predicted_power'], 
                name="AI Prediction", 
                line=dict(color='#00F0FF', width=2, dash='dash')
            ))

            fig.update_layout(
                title="Real-time Power Production vs AI Forecast",
                template="plotly_dark",
                xaxis_title="Measurement ID",
                yaxis_title="Watts (W)",
                height=600,
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            st.write("### Recent Logs")
            st.dataframe(df.tail(5)[['id', 'irradiance', 'temperature', 'power', 'predicted_power']], use_container_width=True)
            
    time.sleep(3)