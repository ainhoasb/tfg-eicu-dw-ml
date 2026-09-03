import pandas as pd
import pyodbc
import yaml
import warnings
import streamlit as st

warnings.filterwarnings('ignore', category=UserWarning)

def get_connection():
    with open('data/config.yaml', 'r') as file:
        db_config = yaml.safe_load(file)['azure_sql']
    
    connection_string = (
        f"DRIVER={db_config['driver']};"
        f"SERVER={db_config['server']};"
        f"PORT=1433;"
        f"DATABASE={db_config['database']};"
        f"UID={db_config['username']};"
        f"PWD={db_config['password']}"
    )
    return pyodbc.connect(connection_string)

@st.cache_data
def load_dw_data():
    conn = get_connection()
    
    # Añadimos TOP 5000 para no colapsar la RAM durante la fase de pruebas
    df_admitted = pd.read_sql("SELECT * FROM vw_Dashboard_AdmittedToICU", conn)
    df_vitals = pd.read_sql("SELECT TOP(100000) * FROM vw_Dashboard_VitalMeasures", conn)
    df_bp = pd.read_sql("SELECT TOP(100000) * FROM vw_Dashboard_BloodPressure", conn)
    df_treatments = pd.read_sql("SELECT TOP(100000) * FROM vw_Dashboard_Treatments", conn)
    df_diagnoses = pd.read_sql("SELECT TOP(100000) * FROM vw_Dashboard_Diagnoses", conn)
    
    conn.close()
    return df_admitted, df_vitals, df_bp, df_treatments, df_diagnoses