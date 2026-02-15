# ☀️ SolarBrain: Intelligent PV Management System

**SolarBrain** is a professional-grade monitoring and predictive analytics platform for Photovoltaic (PV) systems. [cite_start]It bridges the gap between raw **IoT** sensor data and **Machine Learning** to provide real-time insights into energy production and performance forecasting.

## Project Overview
* [cite_start]**Real-Time Monitoring**: Live tracking of Irradiance, Temperature, and Power output through a web-based dashboard[cite: 17].
* [cite_start]**Performance Analysis**: Comparing actual power output against AI-predicted values to identify operational inefficiencies or "Blind Spots" like dust or hardware failures[cite: 13, 18].
* [cite_start]**Production Forecasting**: Leveraging AI to forecast energy generation based on weather parameters to assist in grid management and reduce uncertainty[cite: 14, 19].

## Technical Stack
* [cite_start]**Backend**: Python with **FastAPI**[cite: 69, 70].
* [cite_start]**Frontend**: **HTML5**, **CSS3**, and **JavaScript** with **Plotly.js** for dynamic data visualization[cite: 88, 91].
* [cite_start]**Database**: **SQLite3** for persistent storage of sensor measurements[cite: 49, 50].
* [cite_start]**Machine Learning**: **Random Forest Regressor** for high-accuracy power prediction[cite: 41].

## Project Structure
* [cite_start]`main.py`: The FastAPI server that handles API routes and serves the web interface[cite: 70].
* [cite_start]`sensor_simulation.py`: Simulates IoT hardware by generating and storing live PV data every 3 seconds[cite: 59, 60, 67].
* [cite_start]`database_setup.py`: Script to initialize the SQLite database and the `measurements` table[cite: 48, 50].
* `upgrade_db.py`: Database migration script to add the `predicted_power` column for ML integration.
* [cite_start]`solar_analysis.ipynb`: Jupyter Notebook containing data cleaning, exploratory analysis, and model training[cite: 22].
* [cite_start]`templates/index.html`: The main user interface for the dashboard[cite: 88].
* [cite_start]`solar_model.pkl` & `scaler.pkl`: The exported AI model and data scaler objects[cite: 44, 73].
* `check_db.py` & `clean_db.py`: Utility scripts for database maintenance and verification.

## Machine Learning Logic
[cite_start]The system utilizes a **Random Forest** model trained to predict **AC Power** based on three key features[cite: 34, 41]:
1. [cite_start]**Irradiation**: Solar intensity measured in $W/m^2$[cite: 32, 55].
2. [cite_start]**Ambient Temperature**: Surrounding air temperature[cite: 32].
3. [cite_start]**Module Temperature**: The actual temperature of the solar panels[cite: 33].

## Execution Guide

**Step 1: Initialize the Database** Run the setup script to create the initial SQLite database.  
`python database_setup.py`

**Step 2: Upgrade the Schema** Execute the migration script to add the AI prediction columns.  
`python upgrade_db.py`

**Step 3: Start the IoT Simulation** Launch the simulator to begin generating live solar data.  
`python sensor_simulation.py`

**Step 4: Launch the FastAPI Server** Start the backend server to handle requests and serve the dashboard.  
`uvicorn main:app --reload`

**Step 5: View the Dashboard** Open your browser and navigate to:  
**http://127.0.0.1:8000**
