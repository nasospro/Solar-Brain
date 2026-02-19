# ☀️ SolarBrain: Intelligent PV Management System

**SolarBrain** is a grade monitoring and predictive analytics platform for Photovoltaic (PV) systems. It bridges the gap between raw **IoT** sensor data and **Machine Learning** to provide real-time insights into energy production and performance forecasting.

## Project Overview
* **Real-Time Monitoring**: Live tracking of Irradiance, Temperature, and Power output through a web-based dashboard.
* **Performance Analysis**: Comparing actual power output against AI-predicted values to identify operational inefficiencies or "Blind Spots" like dust or hardware failures.
* **Production Forecasting**: Leveraging AI to forecast energy generation based on weather parameters to assist in grid management and reduce uncertainty.

## Technical Stack
* **Backend**: Python with **FastAPI**.
* **Frontend**: **HTML5**, **CSS3**, and **JavaScript** with **Plotly.js** for dynamic data visualization.
* **Database**: **SQLite3** for persistent storage of sensor measurements.
* **Machine Learning**: **Random Forest Regressor** for high-accuracy power prediction.

## Project Structure
* `main.py`: The FastAPI server that handles API routes and serves the web interface.
* `sensor_simulation.py`: Simulates IoT hardware by generating and storing live PV data every 3 seconds.
* `database_setup.py`: Script to initialize the SQLite database and the `measurements` table.
* `upgrade_db.py`: Database migration script to add the `predicted_power` column for ML integration.
* `solar_analysis.ipynb`: Jupyter Notebook containing data cleaning, exploratory analysis, and model training.
* `templates/index.html`: The main user interface for the dashboard.
* `solar_model.pkl` & `scaler.pkl`: The exported AI model and data scaler objects.
* `check_db.py` & `clean_db.py`: Utility scripts for database maintenance and verification.

## Machine Learning Logic
The system utilizes a **Random Forest** model trained to predict **AC Power** based on three key features:
1. **Irradiation**: Solar intensity measured in $W/m^2$.
2. **Ambient Temperature**: Surrounding air temperature.
3. **Module Temperature**: The actual temperature of the solar panels.

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
