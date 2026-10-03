import streamlit as st
import pandas as pd
import sqlite3
import time
import altair as alt

DB_PATH = '/app/data/metrics.db'

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
        cpu_chart = alt.Chart(metrics_df).mark_line(color='#ff4b4b').encode(
            x=alt.X('timestamp:T', title='Hora', axis=alt.Axis(format='%H:%M:%S', tickCount=6)),
            y=alt.Y('cpu_percent:Q', scale=alt.Scale(domain=[0, 100]), title='CPU %')
        )
        st.altair_chart(cpu_chart, use_container_width=True)
        
    with col2:
        st.subheader("RAM usage (%)")
        ram_chart = alt.Chart(metrics_df).mark_line(color='#0068c9').encode(
            x=alt.X('timestamp:T', title='Hora', axis=alt.Axis(format='%H:%M:%S', tickCount=6)),
            y=alt.Y('ram_percent:Q', scale=alt.Scale(domain=[0, 100]), title='RAM %')
        )
        st.altair_chart(ram_chart, use_container_width=True)

    st.divider()
    
    # Motor de Alertas
    st.subheader("Latest detected alerts (ML)")
    if not alerts_df.empty:
        alerts_df['timestamp'] = pd.to_datetime(alerts_df['timestamp']).dt.strftime('%d/%m/%Y %H:%M:%S')
        st.dataframe(alerts_df, use_container_width=True)
    else:
        st.success("The system is operating within normal parameters. No alerts detected.")

else:
    st.info("Waiting for telemetry data from the sensors...")

# Refresco automático cada 3 segundos
time.sleep(3)
st.rerun()