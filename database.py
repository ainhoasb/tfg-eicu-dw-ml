import pandas as pd
import pyodbc
import yaml
import warnings
import streamlit as st

warnings.filterwarnings('ignore', category=UserWarning)

def get_connection():
    with open('config.yaml', 'r') as file:
        db_config = yaml.safe_load(file)['local_sql']
    
    connection_string = (
        f"DRIVER={db_config['driver']};"
        f"SERVER={db_config['server']};"
        f"DATABASE={db_config['database']};"
        f"Trusted_Connection=yes;"
    )
    return pyodbc.connect(connection_string)

@st.cache_data
def load_dw_data():
    conn = get_connection()
    
    # Añadimos TOP 5000 para no colapsar la RAM durante la fase de pruebas
    df_general = pd.read_sql("SELECT TOP 5000 * FROM vw_Dashboard_General", conn)
    df_vitals = pd.read_sql("SELECT TOP 5000 * FROM vw_Dashboard_VitalMeasures", conn)
    df_bp = pd.read_sql("SELECT TOP 5000 * FROM vw_Dashboard_BloodPressure", conn)
    
    conn.close()
    return df_general, df_vitals, df_bp