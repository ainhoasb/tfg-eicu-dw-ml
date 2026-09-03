"""
Filtrado de los dataframes de resultados de los modelos (clasificación, regresión, 
clustering) usando el mismo diccionario `filters` que devuelve `render_sidebar()`.
 
Los datasets de los notebooks de ML NO tienen todas las columnas del Data
Warehouse -- en concreto, no existen `AdmitYear` ni `Region`, así que esos
dos filtros de la sidebar no tienen ningún efecto sobre las pestañas de
modelos y se ignoran silenciosamente. El resto sí se aplican porque las
columnas equivalentes existen en el dataset de los notebooks:
 
    Filtro sidebar   -> Columna en df de modelos
    --------------------------------------------
    age_range          -> Age
    genders             -> Gender
    ethnicities          -> Ethnicity
    units               -> UnitType
    services            -> Service
    years (AdmitYear)    -> no disponible, se ignora
    regions             -> no disponible, se ignora
"""
 
import pandas as pd
 
 
def filter_model_df(df: pd.DataFrame, filters: dict) -> pd.DataFrame:
    if df is None or df.empty:
        return df
 
    df_filtrado = df
 
    if "Age" in df_filtrado.columns and filters.get("age_range"):
        edad_min, edad_max = filters["age_range"]
        df_filtrado = df_filtrado[df_filtrado["Age"].between(edad_min, edad_max)]

    if filters.get("died_in_hospital"):
            columna_mortalidad = "DiedInHospital" if "DiedInHospital" in df_filtrado.columns else "y_true"
            if columna_mortalidad in df_filtrado.columns:
                df_filtrado = df_filtrado[df_filtrado[columna_mortalidad].isin(filters["died_in_hospital"])]
 
    if "Gender" in df_filtrado.columns and filters.get("genders"):
        df_filtrado = df_filtrado[
            df_filtrado["Gender"].fillna("").astype(str).str.strip().isin(filters["genders"])
        ]
 
    if "Ethnicity" in df_filtrado.columns and filters.get("ethnicities"):
        df_filtrado = df_filtrado[
            df_filtrado["Ethnicity"].fillna("").astype(str).str.strip().isin(filters["ethnicities"])
        ]
 
    if "UnitType" in df_filtrado.columns and filters.get("units"):
        df_filtrado = df_filtrado[df_filtrado["UnitType"].isin(filters["units"])]
 
    if "Service" in df_filtrado.columns and filters.get("services"):
        df_filtrado = df_filtrado[df_filtrado["Service"].isin(filters["services"])]

    
 
    return df_filtrado