import psutil
import sqlite3
import time
from datetime import datetime

def init_db():
    conn = sqlite3.connect('../data/metrics.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS system_metrics
                 (timestamp TEXT, cpu_percent REAL, ram_percent REAL)''')
    conn.commit()
    return conn

def collect_metrics(conn):
    c = conn.cursor()
    while True:
        cpu = psutil.cpu_percent(interval=1)
        ram = psutil.virtual_memory().percent
        now = datetime.now().isoformat()
        
        c.execute("INSERT INTO system_metrics VALUES (?, ?, ?)", (now, cpu, ram))
        conn.commit()
        print(f"[{now}] CPU: {cpu}% | RAM: {ram}%")
        time.sleep(4) # Simula un stream de datos cada 5 segundos

if __name__ == '__main__':
    conn = init_db()
    collect_metrics(conn)