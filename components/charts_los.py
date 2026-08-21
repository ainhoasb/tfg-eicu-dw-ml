"""
Componentes: Regresión de Estancia en UCI - LoS (Notebook 03)
====================================================================
 
Columnas que debe tener `df` (a nivel de paciente, exportado desde el
notebook 03, Poblaciones A y B combinadas en un único parquet):
 
    - Age            : edad
    - Gender          : género
    - Ethnicity        : etnicidad
    - UnitType         : tipo de unidad UCI
    - Service         : área clínica
    - Poblacion        : 'A' (todos los pacientes) o 'B' (solo supervivientes)
    - y_true_dias      : DischargeDayNumber real (escala original, días)
    - y_pred_dias      : estancia predicha por el modelo ganador de esa
                          población (escala original)
 
Columnas que debe tener `df_importancia` (a nivel de variable, exportado
desde las Secciones 4.6 / 5.5 del notebook 03 -- una fila por variable y
población, NO a nivel de paciente, así que no se filtra con la sidebar):
 
    - Poblacion       : 'A' o 'B'
    - Variable          : nombre de la variable predictora
    - Importancia       : importancia según el modelo ganador de esa
                           población (coef_ de Lasso o feature_importances_
                           de Random Forest / XGBoost -- escalas distintas
                           entre poblaciones si el modelo ganador difiere)
    - ModeloGanador      : nombre del modelo ganador de esa población
 
No se recalcula ninguna predicción ni importancia aquí: todo se calculó
una vez en el notebook y se exportó a parquet.
"""
 
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from scipy.stats import gaussian_kde
from sklearn.metrics import mean_absolute_error, mean_squared_error

COLOR_POBLACION = {
    "A": {"etiqueta": "Población A · Todos los pacientes", "color": "#3b82f6", "bg": "#eff6ff"},
    "B": {"etiqueta": "Población B · Solo supervivientes", "color": "#10b981", "bg": "#ecfdf5"},
}

COLOR_REAL = "#6b7280"  # gris neutro, igual para ambas poblaciones
 
 
def _hex_a_rgba(hex_color: str, alpha: float) -> str:
    hex_color = hex_color.lstrip("#")
    r, g, b = tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))
    return f"rgba({r},{g},{b},{alpha})"

def render_poblacion_selector() -> str:
    """Muestra dos botones centrados y coloreados (A / B) y devuelve el código elegido."""
    if "estancia_poblacion" not in st.session_state:
        st.session_state["estancia_poblacion"] = "A"
 
    seleccionada = st.session_state["estancia_poblacion"]
    color_a, color_b = COLOR_POBLACION["A"]["color"], COLOR_POBLACION["B"]["color"]
 
    st.markdown(
        f"""
        <style>
        div.st-key-btn_poblacion_a button {{
            border: 2px solid {color_a} !important;
            color: {"white" if seleccionada == "A" else color_a} !important;
            background-color: {color_a if seleccionada == "A" else "white"} !important;
            font-weight: 600;
            font-size: 1.15rem;
            padding: 0.9rem 1.2rem;
            height: 3.2rem;
        }}
        div.st-key-btn_poblacion_b button {{
            border: 2px solid {color_b} !important;
            color: {"white" if seleccionada == "B" else color_b} !important;
            background-color: {color_b if seleccionada == "B" else "white"} !important;
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
        with st.container(key="btn_poblacion_a"):
            if st.button("Población A · Todos los pacientes", use_container_width=True, key="click_poblacion_a"):
                st.session_state["estancia_poblacion"] = "A"
                st.rerun()
    with col_b:
        with st.container(key="btn_poblacion_b"):
            if st.button("Población B · Solo supervivientes", use_container_width=True, key="click_poblacion_b"):
                st.session_state["estancia_poblacion"] = "B"
                st.rerun()
 
    return st.session_state["estancia_poblacion"]
 
 
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
            <div style="color: #111827; font-size: 2.3rem; font-weight: 800; margin: 6px 0;">{valor}</div>
            <div style="color: #6b7280; font-size: 0.8rem; font-weight: 500;">{subtitulo}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
 
 
def render_kpis(df: pd.DataFrame, codigo_poblacion: str):
    df_poblacion = df[df["Poblacion"] == codigo_poblacion]
    if df_poblacion.empty:
        st.warning("No hay pacientes de esta población que cumplan los filtros seleccionados.")
        return
 
    mae = mean_absolute_error(df_poblacion["y_true_dias"], df_poblacion["y_pred_dias"])
    rmse = np.sqrt(mean_squared_error(df_poblacion["y_true_dias"], df_poblacion["y_pred_dias"]))
 
    color = COLOR_POBLACION[codigo_poblacion]["color"]
    bg = COLOR_POBLACION[codigo_poblacion]["bg"]
    etiqueta_poblacion = COLOR_POBLACION[codigo_poblacion]["etiqueta"]
 
    col1, col2, col3 = st.columns(3)
    with col1:
        _kpi_card(
            "Pacientes",
            f"{len(df_poblacion):,}",
            f"{etiqueta_poblacion} · solo conjunto de test (20% del total)",
            color,
            bg,
        )
    with col2:
        _kpi_card("Error Absoluto Medio (MAE)", f"{mae:.2f} días", "Penaliza todos los errores de forma lineal y proporcional", color, bg)
    with col3:
        _kpi_card("Raíz del Error Cuadrático Medio (RMSE)", f"{rmse:.2f} días", "Penaliza más los errores grandes", color, bg)
 
 
def render_distribution_comparison(df: pd.DataFrame, codigo_poblacion: str):
    """Histogramas superpuestos comparando estancia real vs. predicha, en conteo absoluto de pacientes.
 
    La estancia real ya es un valor entero. Para que la comparación sea justa, la predicha (continua, salida 
    directa del modelo) se redondea con la misma lógica de truncamiento antes de graficar.
    """
    df_poblacion = df[df["Poblacion"] == codigo_poblacion]
    if df_poblacion.empty:
        return
 
    color_predicho = COLOR_POBLACION[codigo_poblacion]["color"]
 
    valores_reales = df_poblacion["y_true_dias"].dropna().to_numpy()
    valores_reales = np.clip(np.round(valores_reales), 0, None).astype(int)
 
    valores_predichos = df_poblacion["y_pred_dias"].dropna().to_numpy()
    valores_predichos = np.clip(np.floor(valores_predichos), 0, None).astype(int)
 
    max_dia = max(valores_reales.max(), valores_predichos.max())
    n_bins = 40
    log_bordes = np.linspace(0, np.log1p(max_dia), n_bins + 1)
    bordes_dias = np.unique(np.round(np.expm1(log_bordes)).astype(int))
 
    counts_reales, _ = np.histogram(valores_reales, bins=bordes_dias)
    counts_predichos, _ = np.histogram(valores_predichos, bins=bordes_dias)
 
    log_bordes_reales = np.log1p(bordes_dias)
    anchos_log = np.diff(log_bordes_reales)
    centros_log = log_bordes_reales[:-1] + anchos_log / 2
 
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=centros_log,
            y=counts_reales,
            width=anchos_log * 0.95,
            name="Estancia real",
            marker=dict(color=COLOR_REAL, line=dict(color="black", width=0.5)),
            opacity=0.55,
        )
    )
    fig.add_trace(
        go.Bar(
            x=centros_log,
            y=counts_predichos,
            width=anchos_log * 0.95,
            name="Estancia predicha",
            marker=dict(color=color_predicho, line=dict(color="black", width=0.5)),
            opacity=0.55,
        )
    )
 
    dias_candidatos = [0, 1, 2, 3, 5, 7, 10, 15, 20, 30, 50, 75, 100, 150, 200, 300, 450]
    limite_dias = max_dia * 1.05
    dias_ticks = [d for d in dias_candidatos if d <= limite_dias]
    fig.update_xaxes(
        tickmode="array",
        tickvals=np.log1p(dias_ticks),
        ticktext=[str(d) for d in dias_ticks],
    )
 
    fig.update_layout(
        title="Distribución de la Estancia Real frente la Predicha (escala logarítmica)",
        xaxis_title="Estancia (días)",
        yaxis_title="Número de pacientes",
        barmode="overlay",
        bargap=0.02,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    st.plotly_chart(fig, use_container_width=True)
 
 
def render_residuals_scatter(df: pd.DataFrame, codigo_poblacion: str):
    df_poblacion = df[df["Poblacion"] == codigo_poblacion].copy()
    if df_poblacion.empty:
        return
 
    df_poblacion["residuo"] = df_poblacion["y_true_dias"] - df_poblacion["y_pred_dias"]
 
    fig = px.scatter(
        df_poblacion,
        x="y_pred_dias",
        y="residuo",
        opacity=0.25,
        labels={"y_pred_dias": "Estancia predicha (días)", "residuo": "Residuo (real - predicho)"},
        title="Residuos vs. Valor Predicho",
    )
    fig.add_hline(y=0, line_dash="dash", line_color="red")
    st.plotly_chart(fig, use_container_width=True)
 
 
def render_residuals_histogram(df: pd.DataFrame, codigo_poblacion: str):
    df_poblacion = df[df["Poblacion"] == codigo_poblacion].copy()
    if df_poblacion.empty:
        return
 
    df_poblacion["residuo"] = df_poblacion["y_true_dias"] - df_poblacion["y_pred_dias"]
 
    fig = go.Figure()
    fig.add_trace(
        go.Histogram(
            x=df_poblacion["residuo"],
            nbinsx=50,
            marker=dict(color="indianred", line=dict(color="black", width=0.5)),
        )
    )
    fig.add_vline(x=0, line_dash="dash", line_color="black")
    fig.update_layout(
        title="Distribución de los Residuos",
        xaxis_title="Residuo (real - predicho, días)",
        yaxis_title="Número de pacientes",
        bargap=0.02,
    )
    st.plotly_chart(fig, use_container_width=True)
 
    st.caption(
        "Nota: estas métricas y gráficas se recalculan sobre el subconjunto filtrado, "
        f"pero usan predicciones ya generadas por el modelo entrenado (Población {codigo_poblacion}). "
        "El modelo no se reentrena con el filtro."
    )
 
 
def render_feature_importance(df_importancia: pd.DataFrame, codigo_poblacion: str, top_n: int = 15):
    if df_importancia is None or df_importancia.empty:
        st.info("No se ha cargado `estancia_importancia.parquet`.")
        return
 
    df_pob = df_importancia[df_importancia["Poblacion"] == codigo_poblacion]
    if df_pob.empty:
        return
 
    modelo_ganador = df_pob["ModeloGanador"].iloc[0]
    top_variables = df_pob.sort_values("Importancia", ascending=False).head(top_n).sort_values("Importancia")
 
    fig = px.bar(
        top_variables,
        x="Importancia",
        y="Variable",
        orientation="h",
        title=f"Top {top_n} Variables Más Importantes del modelo {modelo_ganador} (Población {codigo_poblacion})",
        color_discrete_sequence=[COLOR_POBLACION[codigo_poblacion]["color"]],
    )
    fig.update_layout(yaxis_title="", xaxis_title="Importancia")
    st.plotly_chart(fig, use_container_width=True)

    st.caption(
        "Nota: los filtros de la sidebar no afectan a esta gráfica. La importancia de "
        "variables es una propiedad global del modelo ya entrenado (calculada una vez "
        "sobre todo el conjunto de entrenamiento), no una métrica por paciente"
    )