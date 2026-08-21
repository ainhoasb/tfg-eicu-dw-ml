"""
Componentes: Clasificación de Mortalidad en UCI (Notebook 02)
====================================================================
 
Columnas que debe tener `df` (a nivel de paciente, exportado desde el
notebook 02):
 
    - Age                : edad
    - Gender              : género
    - Ethnicity            : etnicidad
    - UnitType             : tipo de unidad UCI
    - Service             : área clínica
    - APS                 : score de gravedad APACHE Physiology Score
    - y_true              : 0/1, mortalidad real (y_test)
    - y_pred_proba        : probabilidad predicha por el modelo ganador
    - y_pred_default       : predicción binaria con umbral 0.5
    - y_pred_umbral_optimo : predicción binaria con el umbral ajustado (F1)
 
Columnas que debe tener `df_shap` (opcional; Sección 5 del notebook 02 --
SOLO una submuestra de 200 pacientes de test, no todo el conjunto):
 
    - Age, Gender, Ethnicity, UnitType   : para poder filtrar igual que en `df`
    - shap_<variable>  : una columna por variable del modelo, con el valor
                          SHAP de esa variable para ese paciente
 
No se recalcula ninguna predicción ni ningún valor SHAP aquí: todo se
calculó una vez en el notebook y se exportó a parquet.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.metrics import confusion_matrix, classification_report

COLOR_UMBRAL = {
    "y_pred_default": {"etiqueta": "Por defecto (0.5)", "color": "#3b82f6", "bg": "#eff6ff", "escala": "Blues"},
    "y_pred_umbral_optimo": {"etiqueta": "Ajustado (óptimo F1)", "color": "#10b981", "bg": "#ecfdf5", "escala": "Greens"},
}

ESCALA_SHAP = [[0.0, "#0087F7"], [0.5, "#8B5CF6"], [1.0, "#FF0052"]]

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

def render_kpis(df: pd.DataFrame, columna_pred: str):
    if df.empty:
        st.warning("No hay pacientes que cumplan los filtros seleccionados.")
        return
 
    color = COLOR_UMBRAL[columna_pred]["color"]
    bg = COLOR_UMBRAL[columna_pred]["bg"]
    etiqueta_umbral = COLOR_UMBRAL[columna_pred]["etiqueta"]
 
    n_pacientes = len(df)
    n_fallecidos = int(df["y_true"].sum())
    tasa_mortalidad = n_fallecidos / n_pacientes * 100
 
    col1, col2, col3 = st.columns(3)
    with col1:
        _kpi_card("Pacientes", f"{n_pacientes:,}", f"Umbral: {etiqueta_umbral}", color, bg)
    with col2:
        _kpi_card("Fallecimientos", f"{n_fallecidos:,}", "Casos positivos reales (y_true)", color, bg)
    with col3:
        _kpi_card("Tasa de Mortalidad", f"{tasa_mortalidad:.2f}%", "Sobre el conjunto de test filtrado", color, bg)
 
 
def get_umbral_actual() -> str:
    """Lee (o inicializa) la columna de umbral elegida sin dibujar nada."""
    if "mortalidad_umbral_col" not in st.session_state:
        st.session_state["mortalidad_umbral_col"] = "y_pred_default"
    return st.session_state["mortalidad_umbral_col"]
 
 
def render_umbral_selector() -> str:
    """Muestra dos botones de la columna de predicción elegida."""
    seleccionado = get_umbral_actual()
    color_def = COLOR_UMBRAL["y_pred_default"]["color"]
    color_opt = COLOR_UMBRAL["y_pred_umbral_optimo"]["color"]
 
    st.markdown(
        f"""
        <style>
        div.st-key-btn_umbral_default button {{
            border: 2px solid {color_def} !important;
            color: {"white" if seleccionado == "y_pred_default" else color_def} !important;
            background-color: {color_def if seleccionado == "y_pred_default" else "white"} !important;
            font-weight: 600;
            font-size: 1.15rem;
            padding: 0.9rem 1.2rem;
            height: 3.2rem;
        }}
        div.st-key-btn_umbral_optimo button {{
            border: 2px solid {color_opt} !important;
            color: {"white" if seleccionado == "y_pred_umbral_optimo" else color_opt} !important;
            background-color: {color_opt if seleccionado == "y_pred_umbral_optimo" else "white"} !important;
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
        with st.container(key="btn_umbral_default"):
            if st.button("Por defecto (0.5)", use_container_width=True, key="click_umbral_default"):
                st.session_state["mortalidad_umbral_col"] = "y_pred_default"
                st.rerun()
    with col_b:
        with st.container(key="btn_umbral_optimo"):
            if st.button("Ajustado (óptimo F1)", use_container_width=True, key="click_umbral_optimo"):
                st.session_state["mortalidad_umbral_col"] = "y_pred_umbral_optimo"
                st.rerun()
 
    return st.session_state["mortalidad_umbral_col"]
 
 
def render_confusion_matrix(df: pd.DataFrame, columna_pred: str):
    if df.empty:
        return
 
    etiqueta_umbral = COLOR_UMBRAL[columna_pred]["etiqueta"]
    labels = ["Sobrevive", "Fallece"]
    cm = confusion_matrix(df["y_true"], df[columna_pred], labels=[0, 1])
 
    fig = px.imshow(
        cm,
        text_auto=True,
        color_continuous_scale=COLOR_UMBRAL[columna_pred]["escala"],
        x=labels,
        y=labels,
        labels=dict(x="Predicho", y="Real", color="Nº pacientes"),
    )
    fig.update_layout(title=f"Matriz de Confusión ({etiqueta_umbral})", coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True)
 
 
def render_unit_pressure(df: pd.DataFrame, columna_pred: str):
    """Combinado de barras (volumen de pacientes) + línea (% en riesgo) por tipo de unidad UCI."""
    if df.empty:
        return
 
    color = COLOR_UMBRAL[columna_pred]["color"]
 
    tabla = (
        df.groupby("UnitType")
        .agg(n_pacientes=("y_true", "size"), tasa_riesgo=(columna_pred, "mean"))
        .reset_index()
    )
    tabla["tasa_riesgo"] = tabla["tasa_riesgo"] * 100
    tabla = tabla.sort_values("n_pacientes", ascending=False)
 
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=tabla["UnitType"],
            y=tabla["n_pacientes"],
            name="Volumen de pacientes",
            marker=dict(color="#cbd5e1", line=dict(color="black", width=0.5)),
            yaxis="y1",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=tabla["UnitType"],
            y=tabla["tasa_riesgo"],
            name="% Clasificados en riesgo",
            mode="lines+markers",
            line=dict(color=color, width=3),
            marker=dict(size=8),
            yaxis="y2",
        )
    )
    fig.update_layout(
        title=f"Presión Asistencial por Unidad ({COLOR_UMBRAL[columna_pred]['etiqueta']})",
        xaxis_title="Tipo de Unidad",
        yaxis=dict(title="Nº de pacientes", side="left"),
        yaxis2=dict(title="% clasificados en riesgo", side="right", overlaying="y", range=[0, 100]),
        legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="right", x=1),
    )
    st.plotly_chart(fig, use_container_width=True)
 
 
def render_service_risk_heatmap(df: pd.DataFrame):
    """Mapa de calor (columna única) del riesgo medio predicho por servicio médico."""
    if df.empty:
        return
 
    tabla = df.groupby("Service")["y_pred_proba"].mean().sort_values(ascending=False) * 100
    tabla_df = tabla.to_frame(name="Riesgo medio predicho (%)")
 
    fig = px.imshow(
        tabla_df,
        color_continuous_scale="RdYlGn_r",
        text_auto=".1f",
        aspect="auto",
        labels=dict(color="Riesgo predicho (%)"),
    )
    fig.update_layout(
        title="Mapa de Riesgo por Servicio Médico",
        xaxis_title="",
        yaxis_title="",
        height=max(300, 28 * len(tabla_df)),
    )
    fig.update_xaxes(showticklabels=False)
    st.plotly_chart(fig, use_container_width=True)
 
def render_severity_agreement(df: pd.DataFrame, columna_pred: str):
    """Compara el riesgo predicho por el modelo con los scores de gravedad clínica establecidos (APS y/o ApacheScore), 
    agrupando a los pacientes en deciles del score elegido"""
    if df.empty:
        return
 
    columnas_gravedad = [c for c in ["ApacheScore", "APS"] if c in df.columns]
    if not columnas_gravedad:
        st.info(
            "No se han cargado las columnas `APS`/`ApacheScore`"
        )
        return
 
    color = COLOR_UMBRAL[columna_pred]["color"]

    clave_selector = "mortalidad_score_gravedad"
    if clave_selector not in st.session_state or st.session_state[clave_selector] not in columnas_gravedad:
        st.session_state[clave_selector] = columnas_gravedad[0]
    score_elegido = st.session_state[clave_selector]
 
    df_local = df.copy()
    df_local["decil"] = pd.qcut(df_local[score_elegido], 10, duplicates="drop")
 
    resumen = (
        df_local.groupby("decil", observed=True)
        .agg(
            riesgo_predicho=("y_pred_proba", "mean"),
            mortalidad_real=("y_true", "mean"),
            n_pacientes=("y_true", "size"),
            score_medio=(score_elegido, "mean"),
        )
        .reset_index()
        .sort_values("score_medio")
    )
 
    correlacion = df_local[[score_elegido, "y_pred_proba"]].corr(method="spearman").iloc[0, 1]
 
    col_metrica, col_grafico = st.columns([1, 3])
    with col_metrica:
        score_elegido = st.radio(
            "Score de gravedad clínica a comparar:",
            columnas_gravedad,
            horizontal=True,
            key=clave_selector,
        )
        st.metric(f"Correlación (Spearman)\ncon {score_elegido}", f"{correlacion:.3f}")
        st.caption(
            "- 1.0 = concuerdan perfectamente en el orden de gravedad\n"
            "- 0.0 = ninguna relación"
        )
    with col_grafico:
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=resumen["score_medio"],
                y=resumen["riesgo_predicho"],
                mode="lines+markers",
                name="Riesgo medio predicho (modelo)",
                line=dict(width=3, color=color),
            )
        )
        fig.add_trace(
            go.Scatter(
                x=resumen["score_medio"],
                y=resumen["mortalidad_real"],
                mode="lines+markers",
                name="Mortalidad real observada",
                line=dict(width=3, dash="dash", color="#6b7280"),
            )
        )
        fig.update_layout(
            title=f"Riesgo Predicho en comparación con {score_elegido} (por deciles de gravedad)",
            xaxis_title=f"{score_elegido} (media del decil)",
            yaxis_title="Proporción",
            yaxis_tickformat=".0%",
            legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="right", x=1),
        )
        st.plotly_chart(fig, use_container_width=True)
 
    st.caption(
        "Nota: Cada punto agrupa ~10% de los pacientes con gravedad similar (deciles), no pacientes individuales."
    )
 
 
def render_classification_report(df: pd.DataFrame, columna_pred: str):
    """Informe de clasificación (precision/recall/f1/support) como tabla fija y estructurada."""
    if df.empty:
        return
 
    color = COLOR_UMBRAL[columna_pred]["color"]
    reporte = classification_report(
        df["y_true"], df[columna_pred], target_names=["Sobrevive", "Fallece"], output_dict=True
    )
 
    def _fila(etiqueta: str, metricas: dict, estilo: str = "") -> str:
        return f"""
        <tr style="{estilo}">
            <td style="padding: 8px 12px; border-bottom: 1px solid #e5e7eb;">{etiqueta}</td>
            <td style="padding: 8px 12px; border-bottom: 1px solid #e5e7eb; text-align: right;">{metricas['precision']:.3f}</td>
            <td style="padding: 8px 12px; border-bottom: 1px solid #e5e7eb; text-align: right;">{metricas['recall']:.3f}</td>
            <td style="padding: 8px 12px; border-bottom: 1px solid #e5e7eb; text-align: right;">{metricas['f1-score']:.3f}</td>
            <td style="padding: 8px 12px; border-bottom: 1px solid #e5e7eb; text-align: right;">{int(metricas['support']):,}</td>
        </tr>
        """
 
    filas_html = _fila("<b>Sobrevive</b>", reporte["Sobrevive"])
    filas_html += _fila("<b>Fallece</b>", reporte["Fallece"])
    filas_html += f"""
    <tr style="background-color: #f9fafb;">
        <td style="padding: 8px 12px; border-bottom: 1px solid #e5e7eb; font-weight: 600;">Accuracy</td>
        <td style="padding: 8px 12px; border-bottom: 1px solid #e5e7eb;" colspan="2"></td>
        <td style="padding: 8px 12px; border-bottom: 1px solid #e5e7eb; text-align: right; font-weight: 600;">{reporte['accuracy']:.3f}</td>
        <td style="padding: 8px 12px; border-bottom: 1px solid #e5e7eb; text-align: right;">{int(reporte['macro avg']['support']):,}</td>
    </tr>
    """
    filas_html += _fila("<i>Macro avg</i>", reporte["macro avg"], estilo="color: #6b7280;")
    filas_html += _fila("<i>Weighted avg</i>", reporte["weighted avg"], estilo="color: #6b7280;")
 
    st.markdown(f"###### 📄 Informe de Clasificación ({COLOR_UMBRAL[columna_pred]['etiqueta']})")
 
    tabla_html = f"""
    <div style="border: 1px solid #e5e7eb; border-radius: 10px; overflow: hidden;">
        <table style="width: 100%; border-collapse: collapse; font-size: 0.95rem; table-layout: fixed;">
            <colgroup>
                <col style="width: 28%;">
                <col style="width: 18%;">
                <col style="width: 18%;">
                <col style="width: 18%;">
                <col style="width: 18%;">
            </colgroup>
            <thead>
                <tr style="background-color: {color};">
                    <th style="padding: 10px 12px; text-align: left; color: white; font-weight: 700;">Clase</th>
                    <th style="padding: 10px 12px; text-align: right; color: white; font-weight: 700;">Precision</th>
                    <th style="padding: 10px 12px; text-align: right; color: white; font-weight: 700;">Recall</th>
                    <th style="padding: 10px 12px; text-align: right; color: white; font-weight: 700;">F1-Score</th>
                    <th style="padding: 10px 12px; text-align: right; color: white; font-weight: 700;">Support</th>
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
 
 
def _shap_columnas(df_shap: pd.DataFrame):
    return [c for c in df_shap.columns if c.startswith("shap_")]
 
 
def render_shap_note(df_shap: pd.DataFrame):
    if df_shap is None or df_shap.empty:
        st.info(
            "No hay pacientes de la submuestra SHAP que cumplan los filtros seleccionados "
        )
        return False
    return True
 
 
def render_shap_beeswarm(df_shap: pd.DataFrame, top_n: int = 15):
    """Gráfico tipo beeswarm: un punto por (paciente, variable).
 
    El color representa el VALOR de la variable para ese paciente (bajo/alto,
    igual que el beeswarm clásico de la librería `shap`), no el propio valor SHAP.
    """
    if df_shap is None or df_shap.empty:
        return
 
    cols_shap = _shap_columnas(df_shap)
    importancia_media = df_shap[cols_shap].abs().mean().sort_values(ascending=False)
    top_variables = importancia_media.head(top_n).index.tolist()
    variables_abajo_arriba = list(reversed(top_variables))  # trazamos de abajo hacia arriba
 
    tiene_valores_originales = all(
        f"valor_{v.replace('shap_', '')}" in df_shap.columns for v in top_variables
    )
    if not tiene_valores_originales:
        st.caption(
            "Coloreado por el valor SHAP (no por el valor real de la variable) porque "
            "el parquet no tiene columnas `valor_<variable>`"
        )
 
    valor_max_abs_shap = df_shap[top_variables].abs().max().max()
    rng = np.random.default_rng(42)
 
    fig = go.Figure()
    for i, col in enumerate(variables_abajo_arriba):
        nombre_var = col.replace("shap_", "")
        valores_shap = df_shap[col].to_numpy()
        jitter = rng.uniform(-0.35, 0.35, size=len(valores_shap))
 
        if tiene_valores_originales:
            valores_feature = df_shap[f"valor_{nombre_var}"].to_numpy()
            v_min, v_max = valores_feature.min(), valores_feature.max()
            rango = (v_max - v_min) if v_max > v_min else 1
            color_valores = (valores_feature - v_min) / rango  # normalizado 0-1
            marker = dict(
                size=5,
                opacity=0.7,
                color=color_valores,
                colorscale=ESCALA_SHAP,
                cmin=0,
                cmax=1,
                showscale=(i == 0),
                colorbar=dict(title="Valor de<br>la variable", tickvals=[0, 1], ticktext=["Bajo", "Alto"]),
            )
        else:
            marker = dict(
                size=5,
                opacity=0.7,
                color=valores_shap,
                colorscale=ESCALA_SHAP,
                cmin=-valor_max_abs_shap,
                cmax=valor_max_abs_shap,
            )
 
        fig.add_trace(
            go.Scatter(
                x=valores_shap,
                y=np.full(len(valores_shap), i) + jitter,
                mode="markers",
                marker=marker,
                name=nombre_var,
                showlegend=False,
                hovertemplate=f"{nombre_var}: %{{x:.3f}}<extra></extra>",
            )
        )
 
    fig.update_yaxes(
        tickmode="array",
        tickvals=list(range(len(variables_abajo_arriba))),
        ticktext=[v.replace("shap_", "") for v in variables_abajo_arriba],
    )
    fig.add_vline(x=0, line_dash="dash", line_color="gray")
    fig.update_layout(
        title="Impacto de cada variable en la predicción (SHAP)",
        xaxis_title="Valor SHAP (impacto en la predicción)",
        height=450,
    )
    st.plotly_chart(fig, use_container_width=True)
 
 
def render_shap_importance(df_shap: pd.DataFrame, top_n: int = 15):
    if df_shap is None or df_shap.empty:
        return
 
    cols_shap = _shap_columnas(df_shap)
    importancia_media = df_shap[cols_shap].abs().mean().sort_values(ascending=True).tail(top_n)
 
    fig = px.bar(
        x=importancia_media.values,
        y=[c.replace("shap_", "") for c in importancia_media.index],
        orientation="h",
        color=importancia_media.values,
        color_continuous_scale=ESCALA_SHAP,
        labels={"x": "Importancia media |SHAP|", "y": ""},
        title="Importancia media de variables (|SHAP|)",
    )
    fig.update_layout(height=450, coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True)