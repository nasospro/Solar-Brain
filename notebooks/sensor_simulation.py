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
            real_irradiance = random.uniform(0.0, 1000.0)
            scaled_irradiance = (real_irradiance / 1000.0) * 1.22

            # Correlated temperature value based on irradiance
            base_temp = 15.0 + (real_irradiance * 0.02)
            temperature = base_temp + random.uniform(-3.0, 3.0)

            # Calculate actual power output
            raw_val = (real_irradiance * 17.5) - (temperature * 5.0)

            if raw_val > 13200:
                actual_power_output = 13200.0 + random.uniform(-10, 10)
            else:
                actual_power_output = raw_val + random.uniform(-10, 10)

            if actual_power_output < 0:
                actual_power_output = 0.0

            # Insert data into the database
            cursor.execute('''
                    INSERT INTO measurements (irradiance, temperature, power)
                    VALUES (?, ?, ?)
                ''', (scaled_irradiance, temperature, actual_power_output))
            
            conn.commit()

            print(f"Stored: Irr(Scaled): {scaled_irradiance:>4.2f} | Temp: {temperature:>4.1f} C | Power: {actual_power_output:>8.2f} W")

            time.sleep(3)

    
                            
            
    except KeyboardInterrupt: 
        print(f"\nSimulation stopped safely") 
        conn.close()

if __name__ == "__main__":
    run_simulation()     