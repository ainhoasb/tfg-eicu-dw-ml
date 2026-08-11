import streamlit as st
from database import load_dw_data
from components.kpis import render_kpis
from components.charts_general import render_treemap, render_demographics, render_comorbidities
from components.charts_vitals import render_vitals_distribution, render_bp_scatter

st.set_page_config(page_title="Dashboard DW Clínico - TFG", layout="wide")
st.title("📊 Catálogo Analítico - Data Warehouse Clínico")

# 1. Cargar Datos Globales
df_general, df_vitals, df_bp = load_dw_data()

# 2. Barra Lateral de Filtros Globales
st.sidebar.header("🔍 Filtros Globales")

years = sorted(df_general['AdmitYear'].dropna().unique())
selected_years = st.sidebar.multiselect("Año de Ingreso", years, default=years)

regions = sorted(df_general['Region'].dropna().unique())
selected_regions = st.sidebar.multiselect("Región", regions, default=regions)

unit_types = sorted(df_general['UnitType'].dropna().unique())
selected_units = st.sidebar.multiselect("Tipo de Unidad", unit_types, default=unit_types)

# 3. Aplicar Filtro Global
df_filtered = df_general[
    (df_general['AdmitYear'].isin(selected_years)) &
    (df_general['Region'].isin(selected_regions)) &
    (df_general['UnitType'].isin(selected_units))
]

# Filtrar tablas secundarias vinculando con los PatientUnitStayID filtrados
valid_stays = df_filtered['PatientUnitStayID'].dropna().unique()
df_vitals_filtered = df_vitals[df_vitals['PatientUnitStayID'].isin(valid_stays)]
df_bp_filtered = df_bp[df_bp['PatientUnitStayID'].isin(valid_stays)]

# 4. Renderizar KPIs
render_kpis(df_filtered)
st.divider()

# 5. Renderizar Gráficas del DW
render_treemap(df_filtered)

col1, col2 = st.columns(2)
with col1:
    render_demographics(df_filtered)
with col2:
    render_comorbidities(df_filtered)

st.divider()
st.header("📈 Monitorización de Signos Vitales y Tensión Arterial")

col3, col4 = st.columns(2)
with col3:
    render_vitals_distribution(df_vitals_filtered)
with col4:
    render_bp_scatter(df_bp_filtered)