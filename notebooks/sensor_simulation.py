import sqlite3
import time
import random

def run_simulation():
    conn = sqlite3.connect('solar_brain.db')
    cursor = conn.cursor()

    print("--- SolarBrain Sensor Simulation Started ---")
    print("Press Ctrl+C to stop the simulation.")

    try:
        while True:
            # Simulate sensor data
            irradiance = random.uniform(0.0, 1000.0)

            # Correlated temperature value based on irradiance
            base_temp = 15.0 + (irradiance * 0.02)
            temperature = base_temp + random.uniform(-3.0, 3.0)

            # Calculate actual power output
            actual_power_output = (irradiance * 0.15)-(temperature * 0.05) + random.uniform(-2.0, 2.0)
            if actual_power_output < 0:
                actual_power_output = 0.0

            # Insert data into the database
            cursor.execute('''
                    INSERT INTO measurements (irradiance, temperature, power)
                    VALUES (?, ?, ?)
                ''', (irradiance, temperature, actual_power_output))
            
            conn.commit()

            print(f"Stored: Irr: {irradiance:>6.2f} W/m2 | Temp: {temperature:>4.1f} C | Power: {actual_power_output:>7.2f} W")

            time.sleep(3)

    
                            
            
    except KeyboardInterrupt: 
        print(f"\nSimulation stopped safely") 
        conn.close()

if __name__ == "__main__":
    run_simulation()     