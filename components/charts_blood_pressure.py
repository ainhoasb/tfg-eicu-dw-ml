import plotly.express as px
import streamlit as st
import pandas as pd

def categorizar_presion(row):
    """Clasifica la Presión Arterial cruzando Sistólica y Diastólica"""
    sys = row.get('Systolic') 
    dia = row.get('Diastolic')

    if pd.isna(sys) or pd.isna(dia):
        return "Desconocido"

    if sys >= 180 or dia >= 120:
        return "Crisis Hipertensiva"
    elif sys >= 140 or dia >= 90:
        return "Hipertensión (Grado 1-2)"
    elif sys >= 130 or dia >= 85:
        return "Normal-Alta (Alerta)"
    elif sys < 90 or dia < 60:
        return "Hipotensión (Peligro)"
    else:
        return "Óptima / Normal"

def render_bp_scatter(df_bp):
    st.subheader("🩸 Presión Arterial Sistólica vs Diastólica")

    if df_bp.empty or 'Systolic' not in df_bp.columns or 'Diastolic' not in df_bp.columns:
        st.info("Datos insuficientes para generar el diagrama de dispersión de la Presión Arterial.")
        return

    df_plot = df_bp.copy()
    df_plot['Estado Clínico'] = df_plot.apply(categorizar_presion, axis=1)

    color_map = {
        "Óptima / Normal": "#10b981",          
        "Normal-Alta (Alerta)": "#f59e0b",     
        "Hipertensión (Grado 1-2)": "#ef4444", 
        "Crisis Hipertensiva": "#7f1d1d",      
        "Hipotensión (Peligro)": "#3b82f6",    
        "Desconocido": "#9ca3af"               
    }

    # Dibujar el Scatter Plot añadiendo hover_data
    fig = px.scatter(
        df_plot,
        x="Diastolic",
        y="Systolic",
        color="Estado Clínico",
        color_discrete_map=color_map,
        hover_data=["PatientUnitStayID"], # <--- Añade el ID del paciente al tooltip
        opacity=0.75,
        title="Clasificación del Riesgo Cardiovascular"
    )

    # Personalizar la etiqueta flotante (tooltip) para que sea más limpia
    fig.update_traces(
        hovertemplate="<b>Paciente ID: %{customdata[0]}</b><br>" +
                      "Sistólica: %{y} mmHg<br>" +
                      "Diastólica: %{x} mmHg<br>"
    )

    # Añadir líneas de referencia
    fig.add_hline(y=130, line_dash="dot", line_color="#9ca3af", line_width=1)
    fig.add_vline(x=85, line_dash="dot", line_color="#9ca3af", line_width=1)
    
    fig.add_hline(y=90, line_dash="dot", line_color="#9ca3af", line_width=1)
    fig.add_vline(x=60, line_dash="dot", line_color="#9ca3af", line_width=1)

    fig.update_layout(
        xaxis_title="Presión Diastólica (mmHg)",
        yaxis_title="Presión Sistólica (mmHg)",
        legend_title_text="Clasificación Médica",
        margin=dict(t=40, l=10, r=10, b=10),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)"
    )
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#f3f4f6')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#f3f4f6')

    st.plotly_chart(fig, use_container_width=True)