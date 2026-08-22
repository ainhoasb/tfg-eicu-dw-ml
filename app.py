import streamlit as st

from database import load_dw_data
from model_results import load_model_results

from filters.sidebar import render_sidebar
from filters.model_filters import filter_model_df

from components.kpis import render_kpis
from components.charts_general import render_treemap, render_demographics, render_comorbidities, render_top_diagnoses, render_admissions_vs_mortality
from components.charts_treatment import  render_stay_vs_treatment_service
from components.charts_vitals import render_vitals_distribution, render_vitals_boxplots
from components.charts_blood_pressure import render_bp_scatter

from components import charts_mortality, charts_los, charts_clustering, introduction, help


st.set_page_config(page_title="Dashboard Clínico - TFG", layout="wide")

# 1. Cargar Datos
df_admitted, df_vitals, df_bp, df_treatments, df_diagnoses = load_dw_data()
df_mortalidad, df_mortalidad_shap, df_estancia, df_estancia_importancia, df_clustering = load_model_results()

# 2. Renderizar Sidebar y Obtener Filtros
filters = render_sidebar(df_admitted)

# 3. Aplicar Filtros Globales
mask = (
    df_admitted['AdmitYear'].isin(filters['years']) &
    df_admitted['Gender'].fillna('').astype(str).str.strip().isin(filters['genders']) &
    df_admitted['Ethnicity'].fillna('').astype(str).str.strip().isin(filters['ethnicities']) &
    df_admitted['Age'].between(filters['age_range'][0], filters['age_range'][1]) &
    df_admitted['Region'].isin(filters['regions']) &
    df_admitted['UnitType'].isin(filters['units']) &
    df_admitted['Service'].isin(filters['services'])
)

df_filtered = df_admitted[mask]

# Filtrado en cascada para tablas secundarias
valid_stays = df_filtered['PatientUnitStayID'].dropna().unique()
df_vitals_filtered = df_vitals[df_vitals['PatientUnitStayID'].isin(valid_stays)]
df_bp_filtered = df_bp[df_bp['PatientUnitStayID'].isin(valid_stays)]
df_treatments_filtered = df_treatments[df_treatments['PatientUnitStayID'].isin(valid_stays)]
df_diagnoses_filtered = df_diagnoses[df_diagnoses['PatientUnitStayID'].isin(valid_stays)]

# Filtros aplicados también a los resultados de los modelos (no aplican todos los filtros)
df_mortalidad_filtered = filter_model_df(df_mortalidad, filters)
df_mortalidad_shap_filtered = filter_model_df(df_mortalidad_shap, filters)
df_estancia_filtered = filter_model_df(df_estancia, filters)
df_clustering_filtered = filter_model_df(df_clustering, filters)

# 4. Estructura de Pestañas
st.title("📊 Plataforma de Analítica Clínica y Minería de Datos")

# Definición de las Pestañas Principales
tab_intro, tab_dw, tab_mortalidad, tab_estancia, tab_clustering, tab_ayuda = st.tabs([
    "ℹ️ Introducción",
    "🏥 Analítica Descriptiva", 
    "🎯 Clasificación de Mortalidad en UCI",
    "🏨 Regresión de Estancia en UCI",
    "📊 Clustering de Fenotipos Clínicos",
    "❓ Guía de Lectura"])

# ==========================================
# PESTAÑA 1: INTRODUCCIÓN Y CONTEXTO
# ==========================================
with tab_intro:
    introduction.render_intro()

# ==========================================
# PESTAÑA 2: DATA WAREHOUSE
# ==========================================
with tab_dw:
    # Renderizar KPIs
    render_kpis(df_filtered)
    st.divider()

    render_treemap(df_filtered)

    col1, col2 = st.columns(2)
    with col1:
        render_demographics(df_filtered)
    with col2:
        render_comorbidities(df_filtered)

    col3, col4 = st.columns(2)
    with col3:
        render_top_diagnoses(df_filtered)
    with col4:
        render_admissions_vs_mortality(df_filtered)

    render_stay_vs_treatment_service(df_filtered, df_treatments_filtered)

    st.divider()    

    render_vitals_boxplots(df_vitals_filtered)

    st.divider()  

    render_bp_scatter(df_bp_filtered)

# ==========================================
# PESTAÑA 3: CLASIFICACIÓN DE MORTALIDAD
# ==========================================
with tab_mortalidad:
    st.header("🎯 Modelo de Clasificación - Predicción de Mortalidad en UCI")
    st.write(
            """
            Modelo supervisado que predice el **riesgo de fallecimiento** asociado al ingreso de un paciente
            durante su estancia en la UCI, a partir de variables clínicas registradas en las
            primeras horas del ingreso (edad, scores APACHE/APS, comorbilidades, constantes
            vitales). Se compararon Regresión Logística, Random Forest y XGBoost mediante
            validación cruzada repetida, el modelo ganador fue XGBoost y se muestra a continuación.
            """
        )
    st.divider()

    columna_pred = charts_mortality.get_umbral_actual()
    charts_mortality.render_kpis(df_mortalidad_filtered, columna_pred)
    st.divider()
    columna_pred = charts_mortality.render_umbral_selector()
 

    st.subheader("Rendimiento del Modelo")

    col1, col2 = st.columns(2)
    with col1:
        charts_mortality.render_confusion_matrix(df_mortalidad_filtered, columna_pred)
    with col2:
        charts_mortality.render_classification_report(df_mortalidad_filtered, columna_pred)
 
    st.divider()
    st.subheader("Visión Operativa y de Gestión")
    col3, col4 = st.columns(2)
    with col3:
        charts_mortality.render_unit_pressure(df_mortalidad_filtered, columna_pred)
    with col4:
        charts_mortality.render_service_risk_heatmap(df_mortalidad_filtered)

    charts_mortality.render_severity_agreement(df_mortalidad_filtered, columna_pred)
 
    st.divider()
    st.subheader("Interpretabilidad (SHAP)")
    if charts_mortality.render_shap_note(df_mortalidad_shap_filtered):
        col5, col6 = st.columns([3, 2])
        with col5:
            charts_mortality.render_shap_beeswarm(df_mortalidad_shap_filtered)
        with col6:
            charts_mortality.render_shap_importance(df_mortalidad_shap_filtered)

# ==========================================
# PESTAÑA 4: REGRESIÓN DE ESTANCIA (LoS)
# ==========================================
with tab_estancia:
    st.header("🏨 Modelo de Regresión - Predicción de Estancia en UCI")
    st.write(
            """
            Modelo supervisado que predice la **duración de la estancia en UCI** (en días)
            a partir de las variables clínicas del ingreso. Se comparan dos poblaciones: **A** (todos los
            ingresos) y **B** (ingresos sin fallecimiento, como análisis de sensibilidad).
            """
        )
    st.divider()
 
    codigo_poblacion = charts_los.render_poblacion_selector()
    charts_los.render_kpis(df_estancia_filtered, codigo_poblacion)
 
    col1, col2 = st.columns(2)
    with col1:
            charts_los.render_distribution_comparison(df_estancia_filtered, codigo_poblacion)
    with col2:
        # df_estancia_importancia es a nivel de variable (no de ingreso), por eso no pasa por filter_model_df
        # los filtros de la sidebar no le aplican.
        charts_los.render_feature_importance(df_estancia_importancia, codigo_poblacion)
 
    col3, col4 = st.columns(2)
    with col3:
            charts_los.render_residuals_scatter(df_estancia_filtered, codigo_poblacion)
    with col4:
        charts_los.render_residuals_histogram(df_estancia_filtered, codigo_poblacion)
    

# ==========================================
# PESTAÑA 5: CLUSTERING DE FENOTIPOS
# ==========================================
with tab_clustering:
    st.header("📊 Modelo de Clustering - Descubrimiento de Fenotipos Clínicos en UCI")
    st.write(
            """
            Modelo no supervisado (K-Means y GMM) que identifica **fenotipos clínicos** del paciente al ingreso, 
            definidos como subgrupos con patrones similares de comorbilidades, constantes vitales y edad. 
            La variable de mortalidad no participó en el proceso de clustering, sino que se utiliza después 
            a modo de validación para comprobar si los clústeres descubiertos tienen relevancia clínica real.
            """
        )
    st.divider()
 
    columna_cluster = charts_clustering.render_algoritmo_selector()
    color_map_cluster = charts_clustering.build_color_map(df_clustering_filtered, columna_cluster)
 
    charts_clustering.render_kpis(df_clustering_filtered, columna_cluster)
 
    col1, col2 = st.columns(2)
    with col1:
        charts_clustering.render_volume_donut(df_clustering_filtered, columna_cluster, color_map_cluster)
    with col2:
        charts_clustering.render_mortality_by_cluster(df_clustering_filtered, columna_cluster, color_map_cluster)
 
    charts_clustering.render_mortality_table(df_clustering_filtered, columna_cluster)

    st.divider()
 
    charts_clustering.render_comorbidity_heatmap(df_clustering_filtered, columna_cluster)

    st.divider()

    col3, col4 = st.columns(2)
    with col3:
        charts_clustering.render_radar_chart(df_clustering_filtered, columna_cluster, color_map_cluster)
    with col4:
        charts_clustering.render_pca_scatter(df_clustering_filtered, columna_cluster, color_map_cluster)

# ==========================================
# PESTAÑA 6: GUÍA DE LECTURA
# ==========================================
with tab_ayuda:
    help.render_help()