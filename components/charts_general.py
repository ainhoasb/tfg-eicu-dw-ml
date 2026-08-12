import plotly.express as px
import streamlit as st

def render_treemap(df):
    st.subheader("Distribución Jerárquica (Región > Hospital > Servicio)")
    
    # Columnas esperadas de la vista
    col_region = 'Region' if 'Region' in df.columns else None
    col_hosp = 'HospitalID' if 'HospitalID' in df.columns else None
    col_service = 'Service' if 'Service' in df.columns else ('UnitType' if 'UnitType' in df.columns else None)

    path_cols = [c for c in [col_region, col_hosp, col_service] if c is not None]

    if len(path_cols) < 2:
        st.info("No hay suficientes datos disponibles para construir la jerarquía.")
        return

    df_tree = df.copy()

    # Formateamos la etiqueta del Hospital: 'Hospital 73'
    if col_hosp in df_tree.columns:
        df_tree['Hospital_Label'] = df_tree[col_hosp].apply(
            lambda x: f"Hospital {str(x).split('.')[0]}" if str(x).replace('.0','').strip().isdigit() else "Hospital Desconocido"
        )
        path_cols = [c if c != col_hosp else 'Hospital_Label' for c in path_cols]

    # Limpieza de nulos y vacíos
    for col in path_cols:
        df_tree[col] = df_tree[col].fillna('No especificado').astype(str).str.strip()
        df_tree[col] = df_tree[col].replace({'': 'No especificado', 'nan': 'No especificado'})

    # Agrupación de datos
    df_grouped = df_tree.groupby(path_cols).size().reset_index(name='TotalPacientes')
    df_grouped = df_grouped[df_grouped['TotalPacientes'] > 0]

    fig = px.treemap(
        df_grouped,
        path=path_cols,
        values='TotalPacientes',
        color='TotalPacientes',
        color_continuous_scale='Blues',
        title="Navegación visual por región, centro sanitario y servicio médico"
    )

    fig.update_traces(
        texttemplate="%{label}<br>Nº Ingresos: %{value}",
        hovertemplate="<b>%{label}</b><br>Pacientes: %{value:,}<br>Proporción: %{percentParent:.1%}"
    )

    fig.update_layout(margin=dict(t=30, l=10, r=10, b=10))

    st.plotly_chart(fig, width="stretch")

def render_demographics(df):
    st.subheader("Distribución por Edad y Género")
    fig = px.histogram(
        df, 
        x='Age', 
        color='Gender', 
        barmode='group',
        nbins=20,
        labels={'Age': 'Edad', 'count': 'Número de Pacientes'}
    )
    # Cambiado use_container_width=True por width="stretch"
    st.plotly_chart(fig, width="stretch")

def render_comorbidities(df):
    st.subheader("Prevalencia de Comorbilidades")
    comorbidities = ['Diabetes', 'Cirrhosis', 'HepaticFailure', 'MetastaticCancer', 'Leukemia', 'Lymphoma', 'Immunosuppression', 'MI']
    counts = df[comorbidities].sum().reset_index()
    counts.columns = ['Comorbilidad', 'Casos']
    
    fig = px.bar(counts, x='Casos', y='Comorbilidad', orientation='h', color='Casos', color_continuous_scale='Reds')
    # Cambiado use_container_width=True por width="stretch"
    st.plotly_chart(fig, width="stretch")