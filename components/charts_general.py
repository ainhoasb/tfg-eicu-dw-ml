import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import pandas as pd

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

def render_top_diagnoses(df):
    st.subheader("Top 10 Diagnósticos de Ingreso")

    # Comprobamos que exista la columna de diagnósticos
    if 'DiagnosisAdmission' not in df.columns or df.empty:
        st.info("No hay datos de diagnósticos para la selección actual.")
        return

    # Limpiamos nulos y contamos las frecuencias
    df_clean = df.dropna(subset=['DiagnosisAdmission']).copy()
    
    # Extraemos solo los 10 más frecuentes
    top_10 = df_clean['DiagnosisAdmission'].value_counts().nlargest(10).reset_index()
    top_10.columns = ['Diagnóstico', 'Total Pacientes']

    if top_10.empty:
        st.info("No hay diagnósticos registrados con los filtros actuales.")
        return

    # Creamos el gráfico de Donut (hole=0.45 crea el hueco central)
    fig = px.pie(
        top_10,
        names='Diagnóstico',
        values='Total Pacientes',
        hole=0.45,
        title="Causas principales de admisión en UCI",
        color_discrete_sequence=px.colors.sequential.Teal  # Tonos clínicos
    )

    # Configuramos las etiquetas y el tooltip (hover)
    fig.update_traces(
        textposition='inside', 
        textinfo='value+percent',
        hovertemplate="<b>%{label}</b><br>Nº Ingresos: %{value}<br>Representa el %{percent} del Top 10"
    )

    # Movemos la leyenda debajo para que el donut se vea más grande
    fig.update_layout(
        margin=dict(t=40, b=10, l=10, r=10),
        legend=dict(
            orientation="h", 
            yanchor="top", 
            y=-0.1, 
            xanchor="center", 
            x=0.5,
            font=dict(size=10)
        )
    )

    st.plotly_chart(fig, use_container_width=True)

def render_admissions_vs_mortality(df):
    st.subheader("📈 Ingresos y Mortalidad por Servicio Médico")

    # Aseguramos que tenemos la columna Service (la preparamos en tu vista SQL anterior)
    required_cols = ['Service', 'DiedInHospital']
    if df.empty or not all(col in df.columns for col in required_cols):
        st.info("Datos de servicio o mortalidad no disponibles para generar esta gráfica.")
        return

    df_plot = df.copy()

    # 1. Limpiamos los nombres de los servicios
    df_plot['Service'] = df_plot['Service'].fillna('Desconocido').astype(str).str.strip()
    df_plot = df_plot[df_plot['Service'] != '']

    # 2. Conversión segura de la mortalidad (por el problema que vimos antes de los strings)
    def safe_mortality(val):
        val_str = str(val).strip().upper()
        if val_str in ['1', '1.0', 'TRUE', 'EXPIRED', 'DEAD']:
            return 1
        return 0
        
    df_plot['Mortalidad_Num'] = df_plot['DiedInHospital'].apply(safe_mortality)

    # 3. Agrupamos y sumamos
    df_grouped = df_plot.groupby('Service').agg(
        Total_Ingresos=('Service', 'size'),
        Fallecidos=('Mortalidad_Num', 'sum')
    ).reset_index()

    # MEJORA ANALÍTICA: Ordenar de mayor a menor volumen de ingresos
    df_grouped = df_grouped.sort_values(by='Total_Ingresos', ascending=False)
    
    # Filtramos servicios con muy poco volumen (menos de 5 casos) para limpiar la gráfica
    df_grouped = df_grouped[df_grouped['Total_Ingresos'] >= 5]

    # 4. Creación del gráfico con dos capas
    fig = go.Figure()

    # Capa 1: Línea de Total Ingresos (Azul claro de la imagen)
    fig.add_trace(go.Scatter(
        x=df_grouped['Service'],
        y=df_grouped['Total_Ingresos'],
        name='Total Ingresos (Admitted)',
        mode='lines+markers',
        line=dict(color='#0ea5e9', width=3, shape='spline'), # Azul claro, línea suavizada
        marker=dict(size=8, symbol='circle'),
        fill='tozeroy', 
        fillcolor='rgba(14, 165, 233, 0.1)', # Relleno transparente
    ))

    # Capa 2: Línea de Fallecidos (Azul oscuro de la imagen)
    fig.add_trace(go.Scatter(
        x=df_grouped['Service'],
        y=df_grouped['Fallecidos'],
        name='Total Fallecidos (Deceased)',
        mode='lines+markers',
        line=dict(color='#1e3a8a', width=3, shape='spline'), # Azul marino / oscuro
        marker=dict(size=8, symbol='circle'),
        fill='tozeroy',
        fillcolor='rgba(30, 58, 138, 0.3)', # Relleno un poco más denso
    ))

    # 5. Diseño y configuración visual
    fig.update_layout(
        title="Curva de volumen y mortalidad clínica",
        xaxis_title="Especialidad / Servicio",
        yaxis_title="Número de Pacientes",
        hovermode="x unified", # MEJORA VISUAL: Combina las métricas en una sola caja al pasar el ratón
        legend=dict(
            orientation="h", 
            yanchor="bottom", 
            y=1.02, 
            xanchor="right", 
            x=1
        ),
        margin=dict(t=60, l=10, r=10, b=40),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)"
    )
    
    fig.update_xaxes(showgrid=False, tickangle=-45) # Inclina los textos para que no se pisen
    fig.update_yaxes(showgrid=True, gridcolor='#f3f4f6')

    st.plotly_chart(fig, use_container_width=True)