import pandas as pd
from pathlib import Path


# ==========================================================
# RUTAS DEL PROYECTO
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

ruta_admision = (
    BASE_DIR
    / "data"
    / "processed"
    / "conare_admision_limpio.csv"
)

ruta_matricula = (
    BASE_DIR
    / "data"
    / "processed"
    / "conare_matricula_limpio.csv"
)


# ==========================================================
# ENCABEZADO
# ==========================================================

print("\n")
print("========================================")
print("COMPROBACIÓN DE DATASETS")
print("========================================")


# ==========================================================
# COMPROBAR QUE LOS ARCHIVOS EXISTEN
# ==========================================================

print("\n")
print("========================================")
print("COMPROBANDO ARCHIVOS")
print("========================================")


if not ruta_matricula.exists():

    print("\nERROR:")
    print(
        "No se encontró el archivo de matrícula:"
    )
    print(ruta_matricula)

    raise FileNotFoundError(
        ruta_matricula
    )


if not ruta_admision.exists():

    print("\nERROR:")
    print(
        "No se encontró el archivo de admisión:"
    )
    print(ruta_admision)

    raise FileNotFoundError(
        ruta_admision
    )


print("\nArchivos encontrados correctamente.")

print(
    f"\nMatrícula:"
)
print(ruta_matricula)

print(
    f"\nAdmisión:"
)
print(ruta_admision)


# ==========================================================
# CARGAR MATRÍCULA
# ==========================================================

print("\n")
print("========================================")
print("DATASET DE MATRÍCULA")
print("========================================")


df_matricula = pd.read_csv(
    ruta_matricula
)


print(
    f"\nFilas: "
    f"{len(df_matricula)}"
)

print(
    f"Columnas: "
    f"{len(df_matricula.columns)}"
)


print("\nColumnas:")

for columna in df_matricula.columns:

    print(
        f"- {columna}"
    )


print("\nTipos de datos:")

print(
    df_matricula.dtypes
)


# ==========================================================
# CARGAR ADMISIÓN
# ==========================================================

print("\n")
print("========================================")
print("DATASET DE ADMISIÓN")
print("========================================")


df_admision = pd.read_csv(
    ruta_admision
)


print(
    f"\nFilas: "
    f"{len(df_admision)}"
)

print(
    f"Columnas: "
    f"{len(df_admision.columns)}"
)


print("\nColumnas:")

for columna in df_admision.columns:

    print(
        f"- {columna}"
    )


print("\nTipos de datos:")

print(
    df_admision.dtypes
)


# ==========================================================
# COMPROBAR VALORES NULOS
# ==========================================================

print("\n")
print("========================================")
print("VALORES NULOS")
print("========================================")


print("\n--- MATRÍCULA ---")

nulos_matricula = (
    df_matricula
    .isnull()
    .sum()
)

nulos_matricula = (
    nulos_matricula[
        nulos_matricula > 0
    ]
)

if nulos_matricula.empty:

    print(
        "No existen valores nulos."
    )

else:

    print(
        nulos_matricula
    )


print("\n--- ADMISIÓN ---")

nulos_admision = (
    df_admision
    .isnull()
    .sum()
)

nulos_admision = (
    nulos_admision[
        nulos_admision > 0
    ]
)

if nulos_admision.empty:

    print(
        "No existen valores nulos."
    )

else:

    print(
        nulos_admision
    )


# ==========================================================
# COMPROBAR DUPLICADOS
# ==========================================================

print("\n")
print("========================================")
print("DUPLICADOS")
print("========================================")


duplicados_matricula = (
    df_matricula
    .duplicated()
    .sum()
)

duplicados_admision = (
    df_admision
    .duplicated()
    .sum()
)


print(
    f"\nDuplicados en matrícula: "
    f"{duplicados_matricula}"
)

print(
    f"Duplicados en admisión: "
    f"{duplicados_admision}"
)


# ==========================================================
# COMPROBAR COLUMNAS ESPERADAS
# ==========================================================

print("\n")
print("========================================")
print("VALIDACIÓN DE COLUMNAS")
print("========================================")


columnas_matricula_esperadas = [

    "AÑO",
    "TIPO_MATRICULA",
    "UNIVERSIDAD",
    "SEDE_CONARE",
    "REGION_PLANIFICACION_SEDE",
    "GAM_SEDE",
    "CARRERA",
    "GRADO_ACADEMICO",
    "NIVEL_ACADEMICO",
    "NIVEL_CINE",
    "AREA_CONOCIMIENTO",
    "DISCIPLINA",
    "AREA_UNESCO",
    "DISCIPLINA_UNESCO",
    "STEM_MICITT",
    "SEXO",
    "EDAD",
    "PROVINCIA_ESTUDIANTE",
    "CANTON_ESTUDIANTE",
    "ZONA_DE URBANIZACION_ESTUDIANTE",
    "ZONA_URBANO_RURAL_ESTUDIANTE",
    "REGION_PLANIFICACION_ESTUDIANTE",
    "GAM_ESTUDIANTE",
    "PAIS_ESTUDIANTE",
    "TIPO_NACIONALIDAD",
    "CONTINENTE"
]


columnas_admision_esperadas = [

    "CONSECUTIVO",
    "ANO_CONCURSO",
    "SEXO",
    "NACIONALIDAD",
    "RANGO_EDAD",
    "PROVINCIA_RESIDENCIA",
    "CANTON_RESIDENCIA",
    "SEDE",
    "RECINTO",
    "RANGO_NOTA_ADMISION",
    "TIPO_COLEGIO",
    "TIPO_HORARIO_COLEGIO",
    "TIPO_MODALIDAD_COLEGIO",
    "PROVINCIA_COLEGIO",
    "CANTON_COLEGIO",
    "TIPO_PROCESO_ADMISION",
    "CARRERA"
]


# ----------------------------------------------------------
# MATRÍCULA
# ----------------------------------------------------------

faltantes_matricula = [

    columna
    for columna in columnas_matricula_esperadas
    if columna not in df_matricula.columns
]

extras_matricula = [

    columna
    for columna in df_matricula.columns
    if columna not in columnas_matricula_esperadas
]


print("\n--- MATRÍCULA ---")

if not faltantes_matricula:

    print(
        "Todas las columnas esperadas están presentes."
    )

else:

    print(
        "Columnas faltantes:"
    )

    for columna in faltantes_matricula:

        print(
            f"- {columna}"
        )


if extras_matricula:

    print(
        "\nColumnas adicionales:"
    )

    for columna in extras_matricula:

        print(
            f"- {columna}"
        )

else:

    print(
        "No existen columnas adicionales."
    )


# ----------------------------------------------------------
# ADMISIÓN
# ----------------------------------------------------------

faltantes_admision = [

    columna
    for columna in columnas_admision_esperadas
    if columna not in df_admision.columns
]

extras_admision = [

    columna
    for columna in df_admision.columns
    if columna not in columnas_admision_esperadas
]


print("\n--- ADMISIÓN ---")

if not faltantes_admision:

    print(
        "Todas las columnas esperadas están presentes."
    )

else:

    print(
        "Columnas faltantes:"
    )

    for columna in faltantes_admision:

        print(
            f"- {columna}"
        )


if extras_admision:

    print(
        "\nColumnas adicionales:"
    )

    for columna in extras_admision:

        print(
            f"- {columna}"
        )

else:

    print(
        "No existen columnas adicionales."
    )


# ==========================================================
# MOSTRAR PRIMEROS REGISTROS
# ==========================================================

print("\n")
print("========================================")
print("MUESTRA DE LOS DATASETS")
print("========================================")


print("\n--- PRIMEROS 5 REGISTROS DE MATRÍCULA ---")

print(
    df_matricula.head()
)


print("\n--- PRIMEROS 5 REGISTROS DE ADMISIÓN ---")

print(
    df_admision.head()
)


# ==========================================================
# RESUMEN FINAL
# ==========================================================

print("\n")
print("========================================")
print("RESUMEN DE LA COMPROBACIÓN")
print("========================================")


print(
    f"\nMatrícula:"
)

print(
    f"- Filas: {len(df_matricula)}"
)

print(
    f"- Columnas: {len(df_matricula.columns)}"
)

print(
    f"- Duplicados: {duplicados_matricula}"
)


print(
    f"\nAdmisión:"
)

print(
    f"- Filas: {len(df_admision)}"
)

print(
    f"- Columnas: {len(df_admision.columns)}"
)

print(
    f"- Duplicados: {duplicados_admision}"
)


print("\n")
print("========================================")
print("COMPROBACIÓN COMPLETADA")
print("========================================")