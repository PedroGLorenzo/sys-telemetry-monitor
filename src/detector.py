import sqlite3
import pandas as pd
from sklearn.ensemble import IsolationForest
import time
import os


def init_alerts_db():
    conn = sqlite3.connect('/app/data/metrics.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS alerts
                 (timestamp TEXT, cpu_percent REAL, ram_percent REAL, status TEXT)''')
    conn.commit()
    return conn

def run_detector():
    conn = init_alerts_db()
    print("Model started. Searching for anomalies...")
    
    while True:
        try:
            # Analizar los últimos 300 registros
            df = pd.read_sql_query("SELECT * FROM system_metrics ORDER BY timestamp DESC LIMIT 300", conn)
            
            if len(df) < 50:
                time.sleep(5)
                continue

            # Modelo de ML
            model = IsolationForest(contamination=0.05, random_state=42)
            features = df[['cpu_percent', 'ram_percent']]
            df['anomaly'] = model.fit_predict(features)
            
            # Filtrar las anomalías detectadas (-1)
            anomalies = df[df['anomaly'] == -1]
            
            if not anomalies.empty:
                latest = anomalies.iloc[0]
                now = latest['timestamp']
                
                # Evitar alertas duplicadas en el mismo segundo
                existing = pd.read_sql_query(f"SELECT * FROM alerts WHERE timestamp='{now}'", conn)
                if existing.empty:
                    c = conn.cursor()
                    c.execute("INSERT INTO alerts VALUES (?, ?, ?, ?)", 
                              (now, latest['cpu_percent'], latest['ram_percent'], 'ALERTA_CRITICA'))
                    conn.commit()
                    print(f"Anomaly detected in CPU: {latest['cpu_percent']}%")
                    
        except Exception as e:
            pass # Ignorar fallos de lectura si la DB está bloqueada un instante
            
        time.sleep(5) # Evaluar cada 5 segundos

if __name__ == '__main__':
    # Esperar a que el recolector cree la base de datos primero
    time.sleep(3) 
    run_detector()