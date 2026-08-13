import streamlit as st
from database import load_dw_data
from components.sidebar import render_sidebar
from components.kpis import render_kpis
from components.charts_general import render_treemap, render_demographics, render_comorbidities, render_top_diagnoses
from components.charts_vitals import render_vitals_distribution, render_vitals_boxplots
from components.charts_blood_pressure import render_bp_scatter
st.set_page_config(page_title="Dashboard Clínico - TFG", layout="wide")

# 1. Cargar Datos
df_general, df_vitals, df_bp = load_dw_data()

# 2. Renderizar Sidebar y Obtener Filtros
filters = render_sidebar(df_general)

# 3. Aplicar Filtros Globales
mask = (
    df_general['AdmitYear'].isin(filters['years']) &
    df_general['Gender'].fillna('').astype(str).str.strip().isin(filters['genders']) &
    df_general['Ethnicity'].fillna('').astype(str).str.strip().isin(filters['ethnicities']) &
    df_general['Age'].between(filters['age_range'][0], filters['age_range'][1]) &
    df_general['Region'].isin(filters['regions']) &
    df_general['UnitType'].isin(filters['units'])
)

df_filtered = df_general[mask]

# Filtrado en cascada para tablas secundarias
valid_stays = df_filtered['PatientUnitStayID'].dropna().unique()
df_vitals_filtered = df_vitals[df_vitals['PatientUnitStayID'].isin(valid_stays)]
df_bp_filtered = df_bp[df_bp['PatientUnitStayID'].isin(valid_stays)]

# 4. Estructura de Pestañas
st.title("📊 Plataforma de Analítica Clínica y Minería de Datos")

# Definición de las Pestañas Principales
tab_intro, tab_dw, tab_mining = st.tabs([
    "ℹ️ Introducción & Arquitectura",
    "🏥 Analítica Descriptiva", 
    "💻 Minería de Datos"])

# ==========================================
# PESTAÑA 1: INTRODUCCIÓN Y CONTEXTO
# ==========================================
with tab_intro:
    st.header("📌 Trabajo Fin de Grado: Dashboard y Analítica de Datos Clínicos")
    
    col_a, col_b = st.columns([2, 1])
    
    with col_a:
        st.subheader("Objetivo del Proyecto")
        st.write("""
        Este proyecto abarca la **migración y escalado de un almacén de datos clínicos a la nube de Azure**, 
        junto con el diseño de una capa semántica de vistas en SQL Server y la implementación de un 
        dashboard interactivo en Python (Streamlit).
        
        La plataforma está dividida en dos bloques analíticos:
        1. **Analítica Descriptiva (DW):** Exploración multidimensional de ingresos en UCI, demografía, comorbilidades y signos vitales.
        2. **Analítica Predictiva (Data Mining):** Descubrimiento de patrones mediante modelos de machine learning.
        """)
        
    with col_b:
        st.subheader("🛠️ Tecnologías")
        st.markdown("""
        - **Data Warehouse:** Azure SQL / SQL Server
        - **Frontend:** Streamlit
        - **Visualización:** Plotly Express
        - **Procesamiento:** Pandas & Python
        """)

# ==========================================
# PESTAÑA 2: DATA WAREHOUSE
# ==========================================
with tab_dw:
    # Renderizar KPIs
    render_kpis(df_filtered)
    st.divider()

    render_treemap(df_filtered)

    col21, col22 = st.columns(2)
    with col21:
        render_demographics(df_filtered)
    with col22:
        render_comorbidities(df_filtered)

    render_top_diagnoses(df_filtered)

    st.divider()    

    render_vitals_boxplots(df_vitals_filtered)

    st.divider()  

    render_bp_scatter(df_bp_filtered)

    

# ==========================================
# PESTAÑA 3: DATA MINING
# ==========================================
with tab_mining:
    st.header("🔬 Módulo de Minería de Datos y Modelos")
    st.info("Esta sección contendrá los resultados del análisis de clústeres, reglas de asociación y modelos predictivos.")
    # Aquí iremos añadiendo los componentes de Data Mining más adelante