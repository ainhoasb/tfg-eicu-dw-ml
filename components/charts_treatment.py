import plotly.express as px
import pandas as pd
import streamlit as st

import plotly.express as px
import pandas as pd
import streamlit as st

def render_stay_vs_treatment_service(df_general, df_treatments):
    st.subheader("💊 Distribución de Días de Estancia por Servicio de Tratamiento")

    # 1. Validaciones
    if df_general.empty or df_treatments.empty:
        st.info("Datos insuficientes para generar la comparativa.")
        return

    if 'DischargeDayNumber' not in df_general.columns or 'TreatmentService' not in df_treatments.columns:
        st.warning("Faltan columnas necesarias en los orígenes de datos.")
        return

    # 2. Cruce y limpieza
    df_stay = df_general[['PatientUnitStayID', 'DischargeDayNumber']].dropna()
    df_serv = df_treatments[['PatientUnitStayID', 'TreatmentService']].dropna()

    df_merged = pd.merge(df_stay, df_serv, on='PatientUnitStayID', how='inner')
    df_plot = df_merged[df_merged['DischargeDayNumber'] > 0].copy()
    
    df_plot['TreatmentService'] = df_plot['TreatmentService'].astype(str).str.strip()
    df_plot = df_plot[df_plot['TreatmentService'] != '']

    # 3. Ordenar dinámicamente: calculamos la mediana de días de cada servicio
    orden_mediana = df_plot.groupby('TreatmentService')['DischargeDayNumber'].median().sort_values(ascending=True).index

    # 4. Crear el Gráfico de Cajas (Box Plot)
    fig = px.box(
        df_plot,
        x="DischargeDayNumber",
        y="TreatmentService",
        color="TreatmentService",
        category_orders={"TreatmentService": orden_mediana}, # Aplica el orden que hemos calculado
        points="outliers", # Solo dibuja los puntos atípicos para no sobrecargar
        title="Mediana, cuartiles y casos atípicos de ingreso según especialidad",
        color_discrete_sequence=px.colors.qualitative.Safe # Paleta de colores suaves
    )

    # 5. Diseño visual
    # Calculamos el percentil 95 global para recortar el eje X y que un paciente de 100 días no aplaste todo el gráfico
    limite_x = df_plot['DischargeDayNumber'].quantile(0.95)

    fig.update_layout(
        xaxis_title="Días de Estancia en UCI",
        yaxis_title="Servicio de Tratamiento",
        showlegend=False, # Ocultamos leyenda porque los nombres ya están en el eje Y
        margin=dict(t=40, l=10, r=10, b=10),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)"
    )
    
    # Aplicamos el límite al eje X para que la gráfica respire
    fig.update_xaxes(range=[0, limite_x + 2], showgrid=True, gridcolor='#f3f4f6')
    fig.update_yaxes(showgrid=True, gridcolor='#f3f4f6')

    st.plotly_chart(fig, use_container_width=True)