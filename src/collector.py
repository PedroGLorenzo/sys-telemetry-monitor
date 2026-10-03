import psutil
import os

# Forzar a psutil a leer el /proc del sistema operativo anfitrión (Host)
if os.path.exists('/host/proc'):
    psutil.PROCFS_PATH = '/host/proc'

import sqlite3
import time
from datetime import datetime

def init_db():
    conn = sqlite3.connect('/app/data/metrics.db')
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