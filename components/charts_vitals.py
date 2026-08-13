import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

def render_vitals_distribution(df_vitals):
    st.subheader("Distribución de Saturación de Oxígeno (SpO2)")
    fig = px.box(df_vitals, y='SpO2', points="outliers", color_discrete_sequence=['teal'])
    # Cambiado use_container_width=True por width="stretch"
    st.plotly_chart(fig, width="stretch")

def render_vitals_boxplots(df_vitals):
    st.subheader("🩺 Distribución de Signos Vitales Principales")
    
    # Comprobar que las columnas existen en el DataFrame
    required_cols = ['SpO2', 'HeartRate', 'RespiratoryRate']
    if df_vitals.empty or not all(col in df_vitals.columns for col in required_cols):
        st.info("No hay suficientes datos de signos vitales para generar la gráfica.")
        return

    # Crear una figura con 1 fila y 3 columnas
    fig = make_subplots(
        rows=1, cols=3, 
        subplot_titles=("Saturación de O2 (SpO2)", "Frecuencia Cardíaca", "Frecuencia Respiratoria")
    )

    # 1. Boxplot para SpO2
    fig.add_trace(
        go.Box(
            y=df_vitals['SpO2'], 
            name="SpO2", 
            marker_color="#45b6b0", # Tono turquesa (similar al que ya tenías)
            boxpoints='outliers'
        ),
        row=1, col=1
    )
    
    # 2. Boxplot para Frecuencia Cardíaca (HeartRate)
    fig.add_trace(
        go.Box(
            y=df_vitals['HeartRate'], 
            name="FC (lpm)", 
            marker_color="#ef4444", # Tono rojo clínico
            boxpoints='outliers'
        ),
        row=1, col=2
    )

    # 3. Boxplot para Frecuencia Respiratoria (RespiratoryRate)
    fig.add_trace(
        go.Box(
            y=df_vitals['RespiratoryRate'], 
            name="FR (rpm)", 
            marker_color="#3b82f6", # Tono azul
            boxpoints='outliers'
        ),
        row=1, col=3
    )

    # Ajustar el diseño global de la figura
    fig.update_layout(
        showlegend=False,
        height=450,
        margin=dict(t=50, b=40, l=40, r=40),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)"
    )
    
    # Añadir sutiles líneas de cuadrícula a los ejes Y
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#e5e7eb')

    st.plotly_chart(fig, use_container_width=True)