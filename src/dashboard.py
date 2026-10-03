import streamlit as st
import pandas as pd
import sqlite3
import time

DB_PATH = 'data/metrics.db'

st.set_page_config(page_title="Node Sentinel", layout="wide")
st.title("E2E System Telemetry Monitor")
st.markdown("Real-time monitoring and anomaly detection with Machine Learning.")

def load_data():
    try:
        conn = sqlite3.connect(DB_PATH)
        metrics = pd.read_sql_query("SELECT * FROM system_metrics ORDER BY timestamp DESC LIMIT 100", conn)
        alerts = pd.read_sql_query("SELECT * FROM alerts ORDER BY timestamp DESC LIMIT 5", conn)
        return metrics, alerts
    except:
        return pd.DataFrame(), pd.DataFrame()

metrics_df, alerts_df = load_data()

if not metrics_df.empty:
    # Preparar datos para las gráficas
    metrics_df['timestamp'] = pd.to_datetime(metrics_df['timestamp'])
    metrics_df = metrics_df.sort_values('timestamp')
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("CPU usage (%)")
        st.line_chart(metrics_df.set_index('timestamp')['cpu_percent'])
        
    with col2:
        st.subheader("RAM usage (%)")
        st.line_chart(metrics_df.set_index('timestamp')['ram_percent'])

    st.divider()
    
    # Motor de Alertas
    st.subheader("Latest detected alerts (ML)")
    if not alerts_df.empty:
        st.dataframe(alerts_df, use_container_width=True)
    else:
        st.success("The system is operating within normal parameters. No alerts detected.")

else:
    st.info("Waiting for telemetry data from the sensors...")

# Refresco automático cada 3 segundos
time.sleep(3)
st.rerun()