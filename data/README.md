# Datos y backups (fuera del repositorio)

Los siguientes artefactos **no se incluyen en este repositorio**, por su tamaño y por el acuerdo de uso de datos (DUA) de eICU-CRD:

- Backups completos con datos: `.bak` y `.bacpac` de la base de datos de origen (completa y reducida) y del Data Warehouse
- CSV procesados (completo y reducido)

Están alojados en un contenedor privado de Azure Blob Storage, con la siguiente estructura:

```
tfg-backups-privado/
├── csv/
│   ├── completo/       # 7 CSV procesados de la base de datos completa
│   └── reducido/       # 7 CSV procesados de la base de datos reducida
├── dw/
│   └── completo/       # .bak y .bacpac del Data Warehouse completo
└── eicu-crd/
    ├── completa/       # .bak de la base de datos de origen completa
    └── reducida/       # .bak y .bacpac de la base de datos de origen reducida
```

El acceso no es público: se concede bajo petición. Contacta con ainhoasb@uma.es o con los tutores del proyecto para obtener acceso.

Una vez concedido el acceso, la forma recomendada de explorar y descargar los archivos es mediante **Azure Storage Explorer**, conectándose al contenedor con la URL de firma de acceso compartido (SAS) que se te proporcione (Conectar a un recurso de Azure → Directorio o contenedor de blobs → Dirección URL de la firma de acceso compartido (SAS)). Alternativamente, si solo necesitas un archivo concreto, puede descargarse directamente desde el navegador con una URL que incluya la ruta completa del archivo dentro del contenedor seguida del mismo token SAS.

Lo que sí está en este repositorio: el código de ETL (`etl/`), los scripts SQL (`sql/`), los backups **de solo esquema, sin datos** (`database/*/schema/`), los notebooks (`notebooks/`) y el dashboard (`dashboard/`).
