import pandas as pd
import streamlit as st


@st.cache_data
def load_model_results():
    df_mortalidad = pd.read_parquet("data/mortalidad_resultados.parquet")

    df_mortalidad_shap = pd.read_parquet("data/mortalidad_shap.parquet")

    df_estancia = pd.read_parquet("data/estancia_resultados.parquet")

    df_estancia_importancia = pd.read_parquet("data/estancia_importancia.parquet")

    df_clustering = pd.read_parquet("data/clustering_resultados.parquet")
    df_clustering["Cluster_KMeans_Final"] = df_clustering["Cluster_KMeans_Final"].astype(int)
    df_clustering["Cluster_GMM_Final"] = df_clustering["Cluster_GMM_Final"].astype(int)

    return df_mortalidad, df_mortalidad_shap, df_estancia, df_estancia_importancia, df_clustering
