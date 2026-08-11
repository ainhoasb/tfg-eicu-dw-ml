import plotly.express as px
import streamlit as st

def render_treemap(df):
    st.subheader("Distribución Jerárquica de Ingresos (Región > Hospital > Ward)")
    df_tree = df.groupby(['Region', 'HospitalID', 'WardID']).size().reset_index(name='TotalIngresos')
    
    fig = px.treemap(
        df_tree, 
        path=['Region', 'HospitalID', 'WardID'], 
        values='TotalIngresos',
        color='TotalIngresos',
        color_continuous_scale='Blues'
    )
    st.plotly_chart(fig, use_container_width=True)

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
    st.plotly_chart(fig, use_container_width=True)

def render_comorbidities(df):
    st.subheader("Prevalencia de Comorbilidades")
    comorbidities = ['Diabetes', 'Cirrhosis', 'HepaticFailure', 'MetastaticCancer', 'Leukemia', 'Lymphoma', 'Immunosuppression', 'MI']
    counts = df[comorbidities].sum().reset_index()
    counts.columns = ['Comorbilidad', 'Casos']
    
    fig = px.bar(counts, x='Casos', y='Comorbilidad', orientation='h', color='Casos', color_continuous_scale='Reds')
    st.plotly_chart(fig, use_container_width=True)