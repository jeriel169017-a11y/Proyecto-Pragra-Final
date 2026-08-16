import os
import pandas as pd
from sqlalchemy import text

from src.basedatos.gestor_base_datos import GestorBaseDatos


# ==========================================================
# CONFIGURACIÓN
# ==========================================================

SERVIDOR = "localhost"
BASE_DATOS = "DesercionEstudiantil"

RUTA_MATRICULA = os.path.join(
    "data",
    "processed",
    "conare_matricula_limpio.csv"
)

RUTA_ADMISION = os.path.join(
    "data",
    "processed",
    "conare_admision_limpio.csv"
)


# ==========================================================
# CARGAR CSV DE MATRÍCULA
# ==========================================================

def cargar_csv_matricula():

    print("\n========================================")
    print("CARGANDO DATASET DE MATRÍCULA")
    print("========================================")

    if not os.path.exists(RUTA_MATRICULA):

        raise FileNotFoundError(
            f"No se encontró el archivo:\n{RUTA_MATRICULA}"
        )

    df = pd.read_csv(
        RUTA_MATRICULA,
        low_memory=False
    )

    print("\nArchivo cargado correctamente.")
    print(f"Filas: {len(df)}")
    print(f"Columnas: {len(df.columns)}")

    return df


# ==========================================================
# CARGAR CSV DE ADMISIÓN
# ==========================================================

def cargar_csv_admision():

    print("\n========================================")
    print("CARGANDO DATASET DE ADMISIÓN")
    print("========================================")

    if not os.path.exists(RUTA_ADMISION):

        raise FileNotFoundError(
            f"No se encontró el archivo:\n{RUTA_ADMISION}"
        )

    df = pd.read_csv(
        RUTA_ADMISION,
        low_memory=False
    )

    print("\nArchivo cargado correctamente.")
    print(f"Filas: {len(df)}")
    print(f"Columnas: {len(df.columns)}")

    return df


# ==========================================================
# PREPARAR MATRÍCULA PARA SQL
# ==========================================================

def preparar_matricula(df):

    print("\n========================================")
    print("PREPARANDO DATASET DE MATRÍCULA")
    print("========================================")

    df = df.copy()

    # ------------------------------------------------------
    # CORREGIR NOMBRES DE COLUMNAS
    # ------------------------------------------------------

    df.rename(
        columns={
            "AÑO": "ANIO",
            "ZONA_DE URBANIZACION_ESTUDIANTE":
                "ZONA_DE_URBANIZACION_ESTUDIANTE"
        },
        inplace=True
    )

    # ------------------------------------------------------
    # COLUMNAS ESPERADAS
    # ------------------------------------------------------

    columnas_esperadas = [

        "ANIO",
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
        "ZONA_DE_URBANIZACION_ESTUDIANTE",
        "ZONA_URBANO_RURAL_ESTUDIANTE",
        "REGION_PLANIFICACION_ESTUDIANTE",
        "GAM_ESTUDIANTE",
        "PAIS_ESTUDIANTE",
        "TIPO_NACIONALIDAD",
        "CONTINENTE"
    ]

    # ------------------------------------------------------
    # VERIFICAR COLUMNAS
    # ------------------------------------------------------

    columnas_faltantes = [
        columna
        for columna in columnas_esperadas
        if columna not in df.columns
    ]

    if columnas_faltantes:

        raise ValueError(
            "Faltan columnas en el CSV de matrícula:\n"
            + "\n".join(
                f"- {columna}"
                for columna in columnas_faltantes
            )
        )

    # ------------------------------------------------------
    # DEJAR SOLO COLUMNAS NECESARIAS
    # ------------------------------------------------------

    df = df[columnas_esperadas]

    print("\nDataset de matrícula preparado correctamente.")
    print(f"Columnas: {len(df.columns)}")
    print(f"Registros: {len(df)}")

    return df


# ==========================================================
# PREPARAR ADMISIÓN PARA SQL
# ==========================================================

def preparar_admision(df):

    print("\n========================================")
    print("PREPARANDO DATASET DE ADMISIÓN")
    print("========================================")

    df = df.copy()

    # ------------------------------------------------------
    # COLUMNAS ESPERADAS
    # ------------------------------------------------------

    columnas_esperadas = [

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

    # ------------------------------------------------------
    # VERIFICAR COLUMNAS
    # ------------------------------------------------------

    columnas_faltantes = [
        columna
        for columna in columnas_esperadas
        if columna not in df.columns
    ]

    if columnas_faltantes:

        raise ValueError(
            "Faltan columnas en el CSV de admisión:\n"
            + "\n".join(
                f"- {columna}"
                for columna in columnas_faltantes
            )
        )

    # ------------------------------------------------------
    # DEJAR SOLO COLUMNAS NECESARIAS
    # ------------------------------------------------------

    df = df[columnas_esperadas]

    # ------------------------------------------------------
    # ASEGURAR TEXTO EN CARRERA
    # ------------------------------------------------------

    df["CARRERA"] = df["CARRERA"].astype("string")

    # ------------------------------------------------------
    # INFORMACIÓN DE LONGITUD DE CARRERA
    # ------------------------------------------------------

    longitud_maxima = (
        df["CARRERA"]
        .dropna()
        .str.len()
        .max()
    )

    print(
        f"\nLongitud máxima de CARRERA: "
        f"{int(longitud_maxima) if pd.notna(longitud_maxima) else 0} caracteres."
    )

    print("\nDataset de admisión preparado correctamente.")
    print(f"Columnas: {len(df.columns)}")
    print(f"Registros: {len(df)}")

    return df


# ==========================================================
# AJUSTAR ESTRUCTURA DE TABLA DE ADMISIÓN
# ==========================================================

def ajustar_tabla_admision(gestor, df):

    print("\n========================================")
    print("AJUSTANDO ESTRUCTURA DE CONARE_Admision")
    print("========================================")

    # ------------------------------------------------------
    # CALCULAR LONGITUD REAL DE CARRERA
    # ------------------------------------------------------

    longitud_maxima = (
        df["CARRERA"]
        .dropna()
        .str.len()
        .max()
    )

    if pd.isna(longitud_maxima):
        longitud_maxima = 1

    longitud_maxima = int(longitud_maxima)

    # ------------------------------------------------------
    # USAR UN TAMAÑO SEGURO
    #
    # NVARCHAR(500) permite almacenar las carreras completas
    # sin truncarlas.
    # ------------------------------------------------------

    longitud_sql = max(500, longitud_maxima)

    print(
        f"Longitud máxima encontrada en CSV: "
        f"{longitud_maxima}"
    )

    print(
        f"Tamaño configurado para CARRERA: "
        f"NVARCHAR({longitud_sql})"
    )

    # ------------------------------------------------------
    # MODIFICAR LA COLUMNA
    # ------------------------------------------------------

    with gestor.engine.begin() as conexion:

        conexion.execute(
            text(
                f"""
                ALTER TABLE dbo.CONARE_Admision
                ALTER COLUMN CARRERA NVARCHAR({longitud_sql}) NULL
                """
            )
        )

    print(
        "\nColumna CARRERA ajustada correctamente."
    )


# ==========================================================
# LIMPIAR TABLA DE MATRÍCULA
# ==========================================================

def limpiar_tabla_matricula(gestor):

    print("\n========================================")
    print("PREPARANDO TABLA CONARE_Matricula")
    print("========================================")

    with gestor.engine.begin() as conexion:

        conexion.execute(
            text(
                "TRUNCATE TABLE dbo.CONARE_Matricula"
            )
        )

    print(
        "Tabla CONARE_Matricula preparada para nueva carga."
    )


# ==========================================================
# LIMPIAR TABLA DE ADMISIÓN
# ==========================================================

def limpiar_tabla_admision(gestor):

    print("\n========================================")
    print("PREPARANDO TABLA CONARE_Admision")
    print("========================================")

    with gestor.engine.begin() as conexion:

        conexion.execute(
            text(
                "TRUNCATE TABLE dbo.CONARE_Admision"
            )
        )

    print(
        "Tabla CONARE_Admision preparada para nueva carga."
    )


# ==========================================================
# INSERTAR MATRÍCULA
# ==========================================================

def insertar_matricula(gestor, df):

    print("\n========================================")
    print("INSERTANDO DATOS DE MATRÍCULA")
    print("========================================")

    total = len(df)

    print(f"Registros a insertar: {total}")

    df.to_sql(
        name="CONARE_Matricula",
        con=gestor.engine,
        schema="dbo",
        if_exists="append",
        index=False,
        chunksize=1000,
        method=None
    )

    print(
        "\nDatos de matrícula insertados correctamente."
    )


# ==========================================================
# INSERTAR ADMISIÓN
# ==========================================================

def insertar_admision(gestor, df):

    print("\n========================================")
    print("INSERTANDO DATOS DE ADMISIÓN")
    print("========================================")

    total = len(df)

    print(f"Registros a insertar: {total}")

    df.to_sql(
        name="CONARE_Admision",
        con=gestor.engine,
        schema="dbo",
        if_exists="append",
        index=False,
        chunksize=1000,
        method=None
    )

    print(
        "\nDatos de admisión insertados correctamente."
    )


# ==========================================================
# VERIFICAR REGISTROS
# ==========================================================

def verificar_registros(gestor):

    print("\n========================================")
    print("VERIFICANDO REGISTROS EN SQL SERVER")
    print("========================================")

    consulta = """

    SELECT
        'CONARE_Matricula' AS TABLA,
        COUNT(*) AS REGISTROS
    FROM dbo.CONARE_Matricula

    UNION ALL

    SELECT
        'CONARE_Admision' AS TABLA,
        COUNT(*) AS REGISTROS
    FROM dbo.CONARE_Admision;

    """

    resultado = gestor.ejecutar_consulta(
        consulta
    )

    print("\nRESULTADO DE LA CARGA")
    print("----------------------------------------")

    print(
        resultado.to_string(
            index=False
        )
    )

    return resultado


# ==========================================================
# VERIFICAR MUESTRA DE MATRÍCULA
# ==========================================================

def mostrar_matricula(gestor):

    print("\n========================================")
    print("MUESTRA DE CONARE_Matricula")
    print("========================================")

    consulta = """

    SELECT TOP 5 *
    FROM dbo.CONARE_Matricula;

    """

    resultado = gestor.ejecutar_consulta(
        consulta
    )

    print(
        resultado.to_string(
            index=False
        )
    )


# ==========================================================
# VERIFICAR MUESTRA DE ADMISIÓN
# ==========================================================

def mostrar_admision(gestor):

    print("\n========================================")
    print("MUESTRA DE CONARE_Admision")
    print("========================================")

    consulta = """

    SELECT TOP 5 *
    FROM dbo.CONARE_Admision;

    """

    resultado = gestor.ejecutar_consulta(
        consulta
    )

    print(
        resultado.to_string(
            index=False
        )
    )


# ==========================================================
# VERIFICAR LONGITUD DE CARRERA EN SQL
# ==========================================================

def verificar_carrera_admision(gestor):

    print("\n========================================")
    print("VERIFICANDO COLUMNA CARRERA")
    print("========================================")

    consulta = """

    SELECT
        MAX(LEN(CARRERA)) AS LONGITUD_MAXIMA,
        COUNT(*) AS REGISTROS_CON_CARRERA
    FROM dbo.CONARE_Admision;

    """

    resultado = gestor.ejecutar_consulta(
        consulta
    )

    print(
        resultado.to_string(
            index=False
        )
    )

    return resultado


# ==========================================================
# PROCESO PRINCIPAL DE CARGA
# ==========================================================

def cargar_datasets_sql():

    print("\n========================================")
    print("CARGA DE DATASETS A SQL SERVER")
    print("========================================")

    gestor = GestorBaseDatos(
        servidor=SERVIDOR,
        base_datos=BASE_DATOS
    )

    try:

        # --------------------------------------------------
        # 1. CONECTAR
        # --------------------------------------------------

        gestor.conectar()

        # --------------------------------------------------
        # 2. CARGAR CSV
        # --------------------------------------------------

        df_matricula = cargar_csv_matricula()

        df_admision = cargar_csv_admision()

        # --------------------------------------------------
        # 3. PREPARAR DATASETS
        # --------------------------------------------------

        df_matricula = preparar_matricula(
            df_matricula
        )

        df_admision = preparar_admision(
            df_admision
        )

        # --------------------------------------------------
        # 4. PREPARAR TABLAS CONARE
        # --------------------------------------------------

        limpiar_tabla_matricula(
            gestor
        )

        limpiar_tabla_admision(
            gestor
        )

        # --------------------------------------------------
        # 5. AJUSTAR ESTRUCTURA DE ADMISIÓN
        # --------------------------------------------------

        ajustar_tabla_admision(
            gestor,
            df_admision
        )

        # --------------------------------------------------
        # 6. INSERTAR MATRÍCULA
        # --------------------------------------------------

        insertar_matricula(
            gestor,
            df_matricula
        )

        # --------------------------------------------------
        # 7. INSERTAR ADMISIÓN
        # --------------------------------------------------

        insertar_admision(
            gestor,
            df_admision
        )

        # --------------------------------------------------
        # 8. VERIFICAR CANTIDADES
        # --------------------------------------------------

        resultado = verificar_registros(
            gestor
        )

        # --------------------------------------------------
        # 9. VERIFICAR CARRERA
        # --------------------------------------------------

        verificar_carrera_admision(
            gestor
        )

        # --------------------------------------------------
        # 10. MOSTRAR MUESTRAS
        # --------------------------------------------------

        mostrar_matricula(
            gestor
        )

        mostrar_admision(
            gestor
        )

        print("\n========================================")
        print("CARGA SQL COMPLETADA CORRECTAMENTE")
        print("========================================")

        return resultado

    except Exception as error:

        print("\n========================================")
        print("ERROR DURANTE LA CARGA SQL")
        print("========================================")

        print(error)

        raise

    finally:

        gestor.cerrar_conexion()


# ==========================================================
# EJECUCIÓN DIRECTA
# ==========================================================

if __name__ == "__main__":

    cargar_datasets_sql()