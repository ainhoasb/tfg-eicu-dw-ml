import pandas as pd
import streamlit as st


@st.cache_data
def load_model_results():
    df_mortalidad = pd.read_parquet("data/mortalidad_resultados.parquet")
    df_mortalidad_shap = pd.read_parquet("data/mortalidad_shap.parquet")
    df_estancia = pd.read_parquet("data/estancia_resultados.parquet")
    df_clustering = pd.read_parquet("data/clustering_resultados.parquet")
    return df_mortalidad, df_mortalidad_shap, df_estancia, df_clustering
