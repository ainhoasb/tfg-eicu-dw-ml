import plotly.express as px
import streamlit as st

def render_vitals_distribution(df_vitals):
    st.subheader("Distribución de Saturación de Oxígeno (SpO2)")
    fig = px.box(df_vitals, y='SpO2', points="outliers", color_discrete_sequence=['teal'])
    st.plotly_chart(fig, use_container_width=True)

def render_bp_scatter(df_bp):
    st.subheader("Presión Arterial Sistólica vs Diastólica")
    fig = px.scatter(
        df_bp, 
        x='Diastolic', 
        y='Systolic', 
        color='MeanBP_Continuous',
        opacity=0.6,
        labels={'Diastolic': 'Presión Diastólica', 'Systolic': 'Presión Sistólica'}
    )
    st.plotly_chart(fig, use_container_width=True)