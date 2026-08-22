"""
Componentes: Clustering de Fenotipos Clínicos en UCI (Notebook 04)
====================================================================

Columnas que debe tener `df` (a nivel de ingreso, exportado desde el
notebook 04, Modelo Final sin `DiagnosisAdmission`):

    - Age, Gender, Ethnicity, UnitType, Service : para poder filtrar (sidebar)
    - DiedInHospital        : 0/1, mortalidad real (no participó en el clustering)
    - Cluster_KMeans_Final   : etiqueta de clúster (K-Means)
    - Cluster_GMM_Final      : etiqueta de clúster (GMM)
    - PC1, PC2               : coordenadas de los 2 primeros componentes PCA
    - Comorbilidades (0/1)   : Diabetes, Cirrhosis, HepaticFailure,
                                MetastaticCancer, Leukemia, Immunosuppression, MI
    - Vitales de ingreso     : HeartRate_Admission, RespiratoryRate_Admission,
                                MeanBP_Admission, Temperature

No se recalcula ningún clúster, componente PCA, comorbilidad ni vital aquí,
todo se calculó una vez en el notebook y se exportó a parquet.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

COLOR_ALGORITMO = {
    "Cluster_KMeans_Final": {"etiqueta": "K-Means", "color": "#8F6BFF", "bg": "#f5f3ff"},
    "Cluster_GMM_Final": {"etiqueta": "GMM (Gaussian Mixture)", "color": "#FCA65F", "bg": "#fff7ed"},
}
COLOR_REAL = "#6b7280"  # gris neutro para la referencia "media global"

# Paleta cualitativa de alto contraste, compartida entre donut / barras / PCA
# para que un mismo clúster tenga siempre el mismo color en toda la pestaña.
CLUSTER_COLOR_SEQUENCE = px.colors.qualitative.Dark24

COMORBILIDADES = [
    "Diabetes", "Cirrhosis", "HepaticFailure", "MetastaticCancer",
    "Leukemia", "Immunosuppression", "MI",
]

NOMBRES_COMORBILIDAD = {
    "Diabetes": "Diabetes",
    "Cirrhosis": "Cirrosis",
    "HepaticFailure": "Fallo hepático",
    "MetastaticCancer": "Cáncer metastásico",
    "Leukemia": "Leucemia",
    "Immunosuppression": "Inmunosupresión",
    "MI": "Infarto de miocardio",
}

VITALES = ["HeartRate_Admission", "RespiratoryRate_Admission", "MeanBP_Admission", "Temperature", "Age"]

NOMBRES_VITAL = {
    "HeartRate_Admission": "Frec. cardíaca",
    "RespiratoryRate_Admission": "Frec. respiratoria",
    "MeanBP_Admission": "Presión arterial media",
    "Temperature": "Temperatura",
    "Age": "Edad",
}


def _hex_a_rgba(hex_color: str, alpha: float) -> str:
    hex_color = hex_color.lstrip("#")
    r, g, b = tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))
    return f"rgba({r},{g},{b},{alpha})"


def _kpi_card(etiqueta: str, valor: str, subtitulo: str, color: str, bg: str):
    st.markdown(
        f"""
        <div style="
            border-radius: 12px;
            padding: 18px;
            text-align: center;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.08);
            margin-bottom: 10px;
            background-color: {bg};
            border: 1px solid #e5e7eb;
            border-left: 6px solid {color};
        ">
            <div style="color: #6b7280; font-size: 0.9rem; font-weight: 600; text-transform: uppercase;">{etiqueta}</div>
            <div style="color: #111827; font-size: 2.0rem; font-weight: 800; margin: 6px 0;">{valor}</div>
            <div style="color: #6b7280; font-size: 0.8rem; font-weight: 500;">{subtitulo}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

def render_algoritmo_selector() -> str:
    """Muestra dos botones (K-Means / GMM) y devuelve la columna de clúster elegida."""
    if "clustering_algoritmo_col" not in st.session_state:
        st.session_state["clustering_algoritmo_col"] = "Cluster_KMeans_Final"
 
    seleccionado = st.session_state["clustering_algoritmo_col"]
    color_km = COLOR_ALGORITMO["Cluster_KMeans_Final"]["color"]
    color_gmm = COLOR_ALGORITMO["Cluster_GMM_Final"]["color"]
 
    st.markdown(
        f"""
        <style>
        div.st-key-btn_kmeans button {{
            border: 2px solid {color_km} !important;
            color: {"white" if seleccionado == "Cluster_KMeans_Final" else color_km} !important;
            background-color: {color_km if seleccionado == "Cluster_KMeans_Final" else "white"} !important;
            font-weight: 600;
            font-size: 1.15rem;
            padding: 0.9rem 1.2rem;
            height: 3.2rem;
        }}
        div.st-key-btn_gmm button {{
            border: 2px solid {color_gmm} !important;
            color: {"white" if seleccionado == "Cluster_GMM_Final" else color_gmm} !important;
            background-color: {color_gmm if seleccionado == "Cluster_GMM_Final" else "white"} !important;
            font-weight: 600;
            font-size: 1.15rem;
            padding: 0.9rem 1.2rem;
            height: 3.2rem;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )
 
    _, col_a, col_b, _ = st.columns([1.2, 2, 2, 1.2])
    with col_a:
        with st.container(key="btn_kmeans"):
            if st.button("K-Means", use_container_width=True, key="click_kmeans"):
                st.session_state["clustering_algoritmo_col"] = "Cluster_KMeans_Final"
                st.rerun()
    with col_b:
        with st.container(key="btn_gmm"):
            if st.button("GMM (Gaussian Mixture)", use_container_width=True, key="click_gmm"):
                st.session_state["clustering_algoritmo_col"] = "Cluster_GMM_Final"
                st.rerun()
 
    return st.session_state["clustering_algoritmo_col"]
 
 
def build_color_map(df: pd.DataFrame, columna_cluster: str) -> dict:
    """Asigna un color fijo de alto contraste a cada etiqueta de clúster, para
    que el mismo clúster tenga siempre el mismo color en donut/barras/PCA."""
    if df.empty:
        return {}
    etiquetas = sorted(df[columna_cluster].dropna().unique())
    return {
        etiqueta: CLUSTER_COLOR_SEQUENCE[i % len(CLUSTER_COLOR_SEQUENCE)]
        for i, etiqueta in enumerate(etiquetas)
    }
 
 
def render_kpis(df: pd.DataFrame, columna_cluster: str):
    if df.empty:
        st.warning("No hay ingresos que cumplan los filtros seleccionados.")
        return
 
    color = COLOR_ALGORITMO[columna_cluster]["color"]
    bg = COLOR_ALGORITMO[columna_cluster]["bg"]
    etiqueta_algoritmo = COLOR_ALGORITMO[columna_cluster]["etiqueta"]
 
    tasa_global = df["DiedInHospital"].mean() * 100
    resumen = df.groupby(columna_cluster)["DiedInHospital"].agg(["size", "mean"])
    resumen["mean"] = resumen["mean"] * 100
    cluster_mas_numeroso = resumen["size"].idxmax()
    cluster_mayor_riesgo = resumen["mean"].idxmax()
 
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        _kpi_card(
            "Ingresos",
            f"{len(df):,}",
            f"{etiqueta_algoritmo} · {resumen.shape[0]} clústeres",
            color,
            bg,
        )
    with col2:
        _kpi_card("Mortalidad Global", f"{tasa_global:.2f}%", "Referencia del subconjunto filtrado", color, bg)
    with col3:
        _kpi_card(
            "Clúster Más Numeroso",
            f"Clúster {cluster_mas_numeroso}",
            f"{int(resumen.loc[cluster_mas_numeroso, 'size']):,} ingresos",
            color,
            bg,
        )
    with col4:
        _kpi_card(
            "Clúster de Mayor Riesgo",
            f"Clúster {cluster_mayor_riesgo}",
            f"{resumen.loc[cluster_mayor_riesgo, 'mean']:.2f}% mortalidad",
            color,
            bg,
        )
 
 
def render_volume_donut(df: pd.DataFrame, columna_cluster: str, color_map: dict):
    if df.empty:
        return
 
    conteo = df[columna_cluster].value_counts().sort_index()
    etiquetas = [f"Clúster {c}" for c in conteo.index]
    colores = [color_map[c] for c in conteo.index]
 
    fig = go.Figure(
        data=[
            go.Pie(
                labels=etiquetas,
                values=conteo.values,
                hole=0.45,
                marker=dict(colors=colores, line=dict(color="white", width=2)),
                hovertemplate="<b>%{label}</b><br>%{value:,} ingresos<br>%{percent}<extra></extra>",
                textinfo="percent",
            )
        ]
    )
    fig.update_layout(
        title="Volumen de Ingresos por Fenotipo Clínico del Paciente",
        legend=dict(orientation="v", yanchor="middle", y=0.5),
    )
    st.plotly_chart(fig, use_container_width=True)
 
 
def render_mortality_by_cluster(df: pd.DataFrame, columna_cluster: str, color_map: dict):
    if df.empty:
        st.warning("No hay ingresos que cumplan los filtros seleccionados.")
        return
 
    tasa_global = df["DiedInHospital"].mean() * 100
    tabla = (
        df.groupby(columna_cluster)
        .agg(n_ingresos=("DiedInHospital", "size"), tasa_mortalidad=("DiedInHospital", "mean"))
        .reset_index()
    )
    tabla["tasa_mortalidad"] = tabla["tasa_mortalidad"] * 100
    tabla = tabla.sort_values(columna_cluster, ascending=True)
 
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=tabla[columna_cluster].astype(str),
            y=tabla["tasa_mortalidad"],
            marker=dict(
                color=[color_map[c] for c in tabla[columna_cluster]],
                line=dict(color="black", width=0.5),
            ),
            customdata=tabla["n_ingresos"],
            hovertemplate="Clúster %{x}<br>Mortalidad: %{y:.2f}%<br>Ingresos: %{customdata:,}<extra></extra>",
        )
    )
    fig.add_hline(
        y=tasa_global,
        line_dash="dash",
        line_color="black",
        annotation_text=f"Media global ({tasa_global:.2f}%)",
        annotation_position="top left",
        annotation_font=dict(color="black", size=13),
    )
    fig.update_layout(
        title=f"Mortalidad por Clúster ({COLOR_ALGORITMO[columna_cluster]['etiqueta']})",
        xaxis_title="Clúster",
        yaxis_title="Tasa de mortalidad (%)",
        xaxis_type="category",
    )
    st.plotly_chart(fig, use_container_width=True)
 
 
def render_mortality_table(df: pd.DataFrame, columna_cluster: str):
    if df.empty:
        return
 
    color = COLOR_ALGORITMO[columna_cluster]["color"]
 
    tasa_global = df["DiedInHospital"].mean() * 100
    tabla = (
        df.groupby(columna_cluster)
        .agg(Ingresos=("DiedInHospital", "size"), Mortalidad=("DiedInHospital", "mean"))
        .reset_index()
    )
    tabla["Mortalidad"] = tabla["Mortalidad"] * 100
    tabla["Diferencia"] = tabla["Mortalidad"] - tasa_global
    tabla = tabla.rename(columns={columna_cluster: "Clúster"}).sort_values("Mortalidad", ascending=False)
 
    mortalidad_max = max(tabla["Mortalidad"].max(), 1)
 
    st.markdown(f"##### Detalle de Mortalidad por Clúster ({COLOR_ALGORITMO[columna_cluster]['etiqueta']})")
 
    filas_html = ""
    for _, fila in tabla.iterrows():
        ancho_barra = fila["Mortalidad"] / mortalidad_max * 100
        color_diff = "#dc2626" if fila["Diferencia"] > 0 else "#16a34a"
        signo = "+" if fila["Diferencia"] > 0 else ""
        filas_html += f"""
        <tr>
            <td style="padding: 8px 12px; border-bottom: 1px solid #e5e7eb;">Clúster {int(fila['Clúster'])}</td>
            <td style="padding: 8px 12px; border-bottom: 1px solid #e5e7eb; text-align: right;">{int(fila['Ingresos']):,}</td>
            <td style="padding: 8px 12px; border-bottom: 1px solid #e5e7eb;">
                <div style="display: flex; align-items: center; gap: 8px;">
                    <div style="background: #f3f4f6; border-radius: 4px; flex-grow: 1; height: 14px; overflow: hidden;">
                        <div style="background: {color}; width: {ancho_barra:.1f}%; height: 100%;"></div>
                    </div>
                    <span style="min-width: 55px; text-align: right; font-variant-numeric: tabular-nums;">{fila['Mortalidad']:.2f}%</span>
                </div>
            </td>
            <td style="padding: 8px 12px; border-bottom: 1px solid #e5e7eb; text-align: right; color: {color_diff}; font-weight: 600;">{signo}{fila['Diferencia']:.2f} p.p.</td>
        </tr>
        """
 
    tabla_html = f"""
    <div style="border: 1px solid #e5e7eb; border-radius: 10px; overflow: hidden;">
        <table style="width: 100%; border-collapse: collapse; font-size: 0.95rem; table-layout: fixed;">
            <colgroup>
                <col style="width: 15%;">
                <col style="width: 15%;">
                <col style="width: 45%;">
                <col style="width: 25%;">
            </colgroup>
            <thead>
                <tr style="background-color: {color};">
                    <th style="padding: 10px 12px; text-align: left; color: white; font-weight: 700;">Clúster</th>
                    <th style="padding: 10px 12px; text-align: right; color: white; font-weight: 700;">Ingresos</th>
                    <th style="padding: 10px 12px; text-align: left; color: white; font-weight: 700;">Mortalidad</th>
                    <th style="padding: 10px 12px; text-align: right; color: white; font-weight: 700;">Respecto a la Media Global</th>
                </tr>
            </thead>
            <tbody>
                {filas_html}
            </tbody>
        </table>
    </div>
    """
    tabla_html = "\n".join(line.strip() for line in tabla_html.strip().splitlines())
    st.markdown(tabla_html, unsafe_allow_html=True) 
 
def render_comorbidity_heatmap(df: pd.DataFrame, columna_cluster: str):
    st.subheader("Caracterización Clínica de los Clústeres")
    if df.empty:
        return
 
    ordenar_por_carga = st.checkbox(
        "Ordenar clústeres por carga total de comorbilidades (detectar grupos pluripatológicos)",
        value=False,
        key="clustering_orden_comorbilidad",
    )
 
    tabla_comorb = (df.groupby(columna_cluster)[COMORBILIDADES].mean() * 100)
    tabla_comorb.columns = [NOMBRES_COMORBILIDAD[c] for c in COMORBILIDADES]
 
    if ordenar_por_carga:
        orden = tabla_comorb.sum(axis=1).sort_values(ascending=False).index
        tabla_comorb = tabla_comorb.loc[orden]
        tabla_vitales_z = tabla_vitales_z.loc[orden]
 
    tabla_comorb_t = tabla_comorb.T
    tabla_comorb_t.columns = [f"Clúster {c}" for c in tabla_comorb_t.columns]
 
    fig1 = px.imshow(
        tabla_comorb_t,
        color_continuous_scale="Reds",
        text_auto=".1f",
        aspect="auto",
        labels=dict(color="% ingresos"),
    )
    fig1.update_layout(title="Comorbilidades por Clúster (%)")
    st.plotly_chart(fig1, use_container_width=True)
 
 
def render_radar_chart(df: pd.DataFrame, columna_cluster: str, color_map: dict):
    if df.empty:
        return
 
    etiquetas_disponibles = sorted(int(c) for c in df[columna_cluster].dropna().unique())
 
    clave_selector = "clustering_radar_cluster"
    if clave_selector not in st.session_state or st.session_state[clave_selector] not in etiquetas_disponibles:
        st.session_state[clave_selector] = etiquetas_disponibles[0]
    cluster_elegido = st.session_state[clave_selector]
 
    medianas_cluster = df[df[columna_cluster] == cluster_elegido][VITALES].median()
    medianas_global = df[VITALES].median()
 
    minimos = df[VITALES].min()
    maximos = df[VITALES].max()
    rango = (maximos - minimos).replace(0, 1)
 
    normalizado_cluster = (medianas_cluster - minimos) / rango
    normalizado_global = (medianas_global - minimos) / rango
 
    nombres_ejes = [NOMBRES_VITAL[c] for c in VITALES]
    color_cluster = color_map.get(cluster_elegido, COLOR_REAL)
 
    fig = go.Figure()
    fig.add_trace(
        go.Scatterpolar(
            r=list(normalizado_global) + [normalizado_global.iloc[0]],
            theta=nombres_ejes + [nombres_ejes[0]],
            name="Media global",
            line=dict(color=COLOR_REAL, width=2, dash="dash"),
            fill="toself",
            fillcolor=_hex_a_rgba(COLOR_REAL, 0.1),
        )
    )
    fig.add_trace(
        go.Scatterpolar(
            r=list(normalizado_cluster) + [normalizado_cluster.iloc[0]],
            theta=nombres_ejes + [nombres_ejes[0]],
            name=f"Clúster {cluster_elegido}",
            line=dict(color=color_cluster, width=2),
            fill="toself",
            fillcolor=_hex_a_rgba(color_cluster, 0.3),
        )
    )
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 1], showticklabels=False)),
        title=f"Perfil Fisiológico al Ingreso del Clúster {cluster_elegido} frente a la Media Global",
        legend=dict(orientation="h", yanchor="bottom", y=1.08, xanchor="right", x=1),
    )
    st.plotly_chart(fig, use_container_width=True)
 
    cluster_elegido = st.selectbox(
        "Clúster a comparar con la media global",
        etiquetas_disponibles,
        index=etiquetas_disponibles.index(cluster_elegido),
        key=clave_selector,
    )
 
    tabla_valores = pd.DataFrame(
        {
            "Variable": nombres_ejes,
            f"Clúster {cluster_elegido} (mediana)": medianas_cluster.round(1).values,
            "Media global (mediana)": medianas_global.round(1).values,
        }
    )
    st.dataframe(tabla_valores, use_container_width=True, hide_index=True)
 
    st.caption(
        "Nota: Los ejes del radar están normalizados (0-1, min-max sobre el subconjunto filtrado) "
        "para poder compararlos pese a tener unidades distintas. Los valores reales, "
        "con sus correspondientes unidades, se encuentran en la tabla superior." 
    )
 
 
def render_pca_scatter(df: pd.DataFrame, columna_cluster: str, color_map: dict):
    if df.empty:
        return
 
    mapa_str = {str(k): v for k, v in color_map.items()}
    fig = px.scatter(
        df,
        x="PC1",
        y="PC2",
        color=df[columna_cluster].astype(str),
        color_discrete_map=mapa_str,
        opacity=0.35,
        labels={"color": "Clúster"},
        title=f"Proyección espacial en 2D mediante PCA para {COLOR_ALGORITMO[columna_cluster]['etiqueta']}",
    )
    st.plotly_chart(fig, use_container_width=True)

    st.caption(
            "Nota: PC1 y PC2 explican una parte limitada de la varianza total, útil como mapa "
            "exploratorio, no como evidencia definitiva de separación entre clústeres."
        )