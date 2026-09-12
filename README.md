# TFG — Visualización y Extracción de Información Significativa a partir de un Conjunto de Datos Clínico

Trabajo de Fin de Grado de la Universidad de Málaga (UMA). El proyecto construye un Data Warehouse en Azure a partir del dataset [eICU Collaborative Research Database](https://eicu-crd.mit.edu/) (eICU-CRD) y desarrolla tres modelos de minería de datos sobre esos datos: clasificación de mortalidad, regresión del tiempo de estancia y clustering de fenotipos clínicos. Los resultados se exploran en un dashboard interactivo desarrollado con Streamlit.

- **Tutor:** Dr. Rafael Marcos Luque Baena
- **Cotutor:** Dr. Enrique Soler Castillo

## Arquitectura del proyecto

```
eICU-CRD (dataset PhysioNet)
        │
        ▼
CSV de origen ──► notebook de transformación (00) ──► CSV procesados
        │
        ▼
ETL (local o Azure Data Factory) ──► Base de datos de origen ──► Data Warehouse
        │
        ▼
Notebooks de modelado (01–04): preprocesamiento y Machine Learning
        │
        ├─► Exportación de resultados a Parquet (dashboard/data/*.parquet)
        │
        ▼
Dashboard en Streamlit: visualización interactiva
```

El Data Warehouse se ha desplegado en dos escenarios: una arquitectura híbrida local-nube para la base de datos completa, y un despliegue íntegro en Azure para una versión reducida. El detalle completo (diseño del DW, proceso ETL, y los tres modelos) está en la memoria del TFG, entregada por separado.

## Estructura del repositorio

```
├── etl/
│   ├── local/ETL_TFG_local/          # Proyecto Integration Services (SSIS) adaptado a SQL Server local
│   └── cloud/ETL_TFG_azure_v2017/    # Proyecto SSIS adaptado y desplegado en Azure Data Factory
├── sql/
│   ├── create_dw/                    # Script de creación del Data Warehouse
│   ├── views/                        # Vistas SQL que consume el dashboard
│   └── cleanup/                      # Limpieza de tablas temporales e inserción de datos
├── database/
│   ├── eicu-crd/schema/              # Backup .bak de solo esquema (sin datos) de la BD de origen
│   └── dw/schema/                    # Backup .bak de solo esquema (sin datos) del Data Warehouse
├── notebooks/                        # Preprocesamiento y modelos de ML (ver notebooks/README.md)
├── dashboard/                        # Dashboard en Streamlit
│   ├── app.py                        # Punto de entrada
│   ├── database.py                   # Conexión al DW (Azure SQL o SQL local)
│   ├── model_results.py              # Carga de los resultados de los modelos (Parquet)
│   ├── components/                   # Gráficas y secciones del dashboard
│   ├── filters/                      # Barra lateral y lógica de filtrado
│   ├── images/                       # Logo y assets visuales del dashboard
│   └── data/
│       ├── config_example.yaml       # Plantilla de configuración de conexión (copiar a config.yaml)
│       └── *.parquet                 # Resultados de los notebooks (generados localmente, no versionados)
├── data/
│   └── README.md                     # Puntero de acceso a los datos completos (Azure Blob Storage)
└── requirements.txt
```

Los backups de esquema en `database/` no incluyen datos: sirven para instanciar la estructura de tablas sin necesidad de disponer del dataset completo. Los backups con datos reales (`.bak`/`.bacpac` completos) y los CSV procesados no están en este repositorio por su tamaño y por el acuerdo de uso de datos de eICU-CRD — ver [`data/README.md`](data/README.md) para solicitar acceso.

## Requisitos previos

- Python 3.10 o superior
- Driver ODBC de SQL Server (`ODBC Driver 17 for SQL Server`)
- Acceso a un Data Warehouse en Azure SQL, o una instancia local de SQL Server con el mismo esquema

## Instalación

1. Clona el repositorio:
   ```bash
   git clone https://github.com/ainhoasb/tfg-eicu-dw-ml.git
   cd tfg-eicu-dw-ml
   ```
2. Crea y activa un entorno virtual:
   ```bash
   python -m venv venv_tfg
   # Windows
   venv_tfg\Scripts\activate
   # Linux / macOS
   source venv_tfg/bin/activate
   ```
3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

## Configuración de la conexión

1. Copia la plantilla de configuración:
   ```bash
   cp dashboard/data/config_example.yaml dashboard/data/config.yaml
   ```
2. Edita `dashboard/data/config.yaml` con tus credenciales de Azure SQL, o cambia `active_connection` a `local_sql` para usar una instancia local. Este mismo archivo lo usan tanto el dashboard como el notebook `01_Limpieza_y_Preprocesamiento.ipynb`.

   `config.yaml` está en `.gitignore`: cada persona mantiene su propia copia local, nunca se sube al repositorio.

## Uso

### 1. Notebooks (preprocesamiento y modelado)

Ejecutar en orden desde `notebooks/`. El detalle de cada uno está en [`notebooks/README.md`](notebooks/README.md). Los notebooks 02, 03 y 04 exportan sus resultados a `dashboard/data/*.parquet`, necesarios para que el dashboard funcione.

### 2. Dashboard

Con `dashboard/data/config.yaml` configurado y los `.parquet` generados:

```bash
cd dashboard
streamlit run app.py
```

El dashboard incluye una pestaña por modelo (clasificación, regresión, clustering) más una introducción, con filtros en la barra lateral (edad, sexo, servicio, año de ingreso, estado al alta, etc.) que actúan sobre las visualizaciones sin recalcular los modelos.

## Acceso a los datos completos

Los backups completos de las bases de datos y los CSV procesados están alojados en un contenedor privado de Azure Blob Storage y se facilitan bajo petición, tal como se detalla en [`data/README.md`](data/README.md).

## Memoria

La memoria completa del TFG, incluyendo la metodología del ETL, el diseño del Data Warehouse y el detalle de los tres modelos, se entrega por separado en formato PDF.
