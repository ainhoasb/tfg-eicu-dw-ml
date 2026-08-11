import streamlit as st

def render_kpis(df):
    total_ingresos = len(df)
    mortalidad = (df['DiedInHospital'].sum() / total_ingresos * 100) if total_ingresos > 0 else 0
    apache_avg = df['ApacheScore'].mean() if total_ingresos > 0 else 0
    vent_pct = (df['Vent'].sum() / total_ingresos * 100) if total_ingresos > 0 else 0

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Ingresos UCI", f"{total_ingresos:,}")
    col2.metric("Mortalidad Hospitalaria", f"{mortalidad:.1f}%")
    col3.metric("Apache Score Medio", f"{apache_avg:.1f}")
    col4.metric("% Ventilación Mecánica", f"{vent_pct:.1f}%")