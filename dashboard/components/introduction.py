import streamlit as st


def render_intro():
    st.header("📌 Trabajo Fin de Grado: Visualización y Extracción de Información Significativa a partir de un Conjunto de Datos Clínico")
    st.caption("Ainhoa Nerea Santana Bastante · Universidad de Málaga · Ingeniería de la Salud · 2026")

    st.write(
        """
        Este *dashboard* es el entregable final de un **Trabajo Fin de Grado** centrado en dos
        disciplinas complementarias de la analítica de datos clínicos. El diseño de un
        **Data Warehouse (DW)** en la nube y la aplicación de **Machine Learning** sobre esos
        mismos datos para predecir la mortalidad, la estancia hospitalaria y descubrir fenotipos
        clínicos de pacientes en UCI.
        """
    )

    st.divider()

    col_a, col_b = st.columns(2)

    with col_a:
        st.subheader("🗄️ Origen de los Datos")
        st.write(
            """
            Los datos provienen de **eICU Collaborative Research Database**, una base de datos
            multicéntrica de cuidados intensivos (más de 200 UCIs de EE. UU.), de acceso público
            para investigadores acreditados. A partir de ese origen se construyó un proceso ETL
            (SSIS) que puebla un **Data Warehouse en Azure SQL**, cuyo hecho principal es el
            **ingreso en UCI**. El ingreso es la unidad de análisis de todo este
            dashboard, tanto en la parte descriptiva como en los tres modelos predictivos.
            """
        )

    with col_b:
        st.subheader("🛠️ Arquitectura y Tecnologías")
        st.markdown(
            """
            ```
            eICU (origen)
                 │  ETL (SSIS)
                 ▼
            Azure SQL DW  ──────────────┐
                 │                      │
                 │ vistas SQL           │ Gold Dataset (Python)
                 ▼                      ▼
            Analítica Descriptiva   Notebooks (scikit-learn / XGBoost)
                 │                      │
                 └──────────┬───────────┘
                            ▼
                  Dashboard (Streamlit + Plotly)
            ```
            """
        )

    st.divider()

    st.subheader("🧭 Estructura del Dashboard")
    st.markdown(
        """
        - **🏥 Analítica Descriptiva:** exploración multidimensional del DW, volumen de
          ingresos, demografía, comorbilidades, signos vitales y presión arterial.
        - **🎯 Clasificación de Mortalidad:** modelo que predice el riesgo de fallecimiento de
          un ingreso a partir de variables clínicas de las primeras horas.
        - **🏨 Regresión de Estancia:** modelo que predice la duración de la estancia en UCI,
          comparando todos los ingresos frente a los que terminaron sin fallecimiento.
        - **📊 Clustering de Fenotipos:** modelo no supervisado que agrupa a los pacientes en
          fenotipos clínicos según su perfil al ingreso, validado después con la mortalidad real.
        - **❓ Guía de Lectura:** explicación de términos y de cómo interpretar las gráficas más
          técnicas (SHAP, deciles de gravedad, PCA...), organizada por pestaña.
        """
    )

    st.divider()

    st.subheader("⚠️ Alcance y Limitaciones")
    st.markdown(
        """
        - Los tres modelos se entrenaron sobre un **Gold Dataset de 162.009 ingresos**. Los
          resultados que se ven en sus pestañas provienen del conjunto de test (o del dataset
          completo en el caso del clustering, al ser no supervisado).
        - Algunas vistas del **Data Warehouse** (pestaña "Analítica Descriptiva") están limitadas
          actualmente a una muestra, se debe ajustar el `TOP` de las consultas en
          `database.py` si necesitas explotar el DW completo.
        - Este dashboard es un **proyecto académico con fines didácticos**.
        """
    )