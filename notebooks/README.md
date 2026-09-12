# Notebooks

Los cuadernos 01 a 04 se ejecutan en orden: cada uno depende de los datos que genera el anterior. Requieren `dashboard/data/config.yaml` configurado (ver README principal) para leer del Data Warehouse en Azure SQL o en local.

## 00 — Transformación y Limpieza de los CSV de Origen (`00_Transformacion_y_Limpieza_CSV.ipynb`)

No forma parte de la secuencia de modelado: es un paso preparatorio de la **ETL**, previo a cargar los datos en la base de datos de origen. Transforma los CSV de origen de eICU-CRD (que concatenan varios niveles de información con `/` o `|`, como `pasthistorypath` o `treatmentstring`) en los CSV "procesados" que después carga el proyecto ETL.

Lee los CSV de origen desde `../data/csv_origen/` y exporta los procesados a `../data/CSV_filtrados/` — ninguna de las dos carpetas se versiona en git (datos restringidos de eICU-CRD).

## 01 — Limpieza y Preprocesamiento (`01_Limpieza_y_Preprocesamiento.ipynb`)

Carga los datos del Data Warehouse, previene fugas de datos (*data leakage*) y realiza el análisis exploratorio: auditoría de variables categóricas, booleanas y numéricas, y detección de valores atípicos fisiológicos usando los rangos definidos en `clinical_limits.json` (en esta misma carpeta). Genera el Gold Dataset en CSV y Parquet, en `datos_procesados/`, que usan los tres notebooks de modelado siguientes.

## 02 — Clasificación de Mortalidad (`02_Modelo_Clasificacion_Mortalidad.ipynb`)

Modelo de clasificación para predecir `DiedInHospital`. Incluye codificación categórica, comparación de modelos y análisis de asociación bivariante. Modelo ganador: **XGBoost**.

**Exporta:** `dashboard/data/mortalidad_resultados.parquet`, `dashboard/data/mortalidad_shap.parquet`

## 03 — Regresión de la Estancia (`03_Modelo_Regresion_Estancia.ipynb`)

Modelo de regresión para predecir la duración de la estancia (`DischargeDayNumber`), comparado sobre dos poblaciones: población completa y solo supervivientes. Incluye validación cruzada repetida (RMSE y MAE). Modelo ganador en ambas poblaciones: **XGBoost**.

**Exporta:** `dashboard/data/estancia_resultados.parquet`, `dashboard/data/estancia_importancia.parquet`

## 04 — Clustering de Fenotipos Clínicos (`04_Modelo_Clustering_Fenotipos.ipynb`)

Descubrimiento de fenotipos clínicos mediante K-Means y Gaussian Mixture Models, con PCA previo y Silhouette Score sobre una submuestra de ~5.000 pacientes. Modelo final: **K-Means (k=15)** y **GMM (n=13)**, sin la variable `DiagnosisAdmission`. Incluye validación post-hoc con la tasa de mortalidad por clúster.

**Exporta:** `dashboard/data/clustering_resultados.parquet`

---

Los Parquet exportados por los notebooks 02, 03 y 04 son los que consume el dashboard (`dashboard/model_results.py`). No están versionados en el repositorio: hay que ejecutar los notebooks localmente para generarlos antes de lanzar `streamlit run app.py`.
