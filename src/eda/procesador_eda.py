import os
import pandas as pd


class ProcesadorEDA:
    """
    Clase encargada de realizar el Análisis Exploratorio
    de Datos (EDA) sobre los datasets procesados.

    En esta etapa:

    - No se modifican los datasets originales.
    - No se eliminan registros.
    - No se realizan transformaciones.
    - Se analizan características estructurales,
      estadísticas y distribuciones de los datos.
    """

    def __init__(self, ruta_matricula, ruta_admision):

        self.ruta_matricula = ruta_matricula
        self.ruta_admision = ruta_admision

        self.df_matricula = None
        self.df_admision = None

    # ==========================================================
    # CARGAR DATASETS PROCESADOS
    # ==========================================================

    def cargar_datasets(self):
        """
        Carga los dos datasets previamente limpiados.
        """

        print("\n========================================")
        print("CARGANDO DATASETS PROCESADOS PARA EDA")
        print("========================================")

        if not os.path.exists(self.ruta_matricula):
            raise FileNotFoundError(
                f"No se encontró el archivo de matrícula:\n"
                f"{self.ruta_matricula}"
            )

        if not os.path.exists(self.ruta_admision):
            raise FileNotFoundError(
                f"No se encontró el archivo de admisión:\n"
                f"{self.ruta_admision}"
            )

        self.df_matricula = pd.read_csv(
            self.ruta_matricula
        )

        self.df_admision = pd.read_csv(
            self.ruta_admision
        )

        print("\nDataset de matrícula cargado.")
        print(
            f"Filas: {self.df_matricula.shape[0]}"
        )
        print(
            f"Columnas: {self.df_matricula.shape[1]}"
        )

        print("\nDataset de admisión cargado.")
        print(
            f"Filas: {self.df_admision.shape[0]}"
        )
        print(
            f"Columnas: {self.df_admision.shape[1]}"
        )

    # ==========================================================
    # INFORMACIÓN GENERAL
    # ==========================================================

    def informacion_general(self):
        """
        Muestra la estructura general de ambos datasets.
        """

        print("\n========================================")
        print("INFORMACIÓN GENERAL DEL EDA")
        print("========================================")

        print("\n--- DATASET DE MATRÍCULA ---")

        print(
            f"Filas: {self.df_matricula.shape[0]}"
        )

        print(
            f"Columnas: {self.df_matricula.shape[1]}"
        )

        print("\nColumnas:")

        for columna in self.df_matricula.columns:
            print(f"- {columna}")

        print("\nTipos de datos:")

        print(
            self.df_matricula.dtypes
        )

        print("\n--- DATASET DE ADMISIÓN ---")

        print(
            f"Filas: {self.df_admision.shape[0]}"
        )

        print(
            f"Columnas: {self.df_admision.shape[1]}"
        )

        print("\nColumnas:")

        for columna in self.df_admision.columns:
            print(f"- {columna}")

        print("\nTipos de datos:")

        print(
            self.df_admision.dtypes
        )

    # ==========================================================
    # VALORES NULOS
    # ==========================================================

    def analizar_nulos(self):
        """
        Analiza los valores nulos de ambos datasets.
        """

        print("\n========================================")
        print("ANÁLISIS DE VALORES NULOS")
        print("========================================")

        print("\n--- DATASET DE MATRÍCULA ---")

        nulos_matricula = (
            self.df_matricula
            .isnull()
            .sum()
        )

        nulos_matricula = (
            nulos_matricula[
                nulos_matricula > 0
            ]
        )

        if len(nulos_matricula) == 0:
            print("No existen valores nulos.")
        else:
            print(nulos_matricula)

        print("\n--- DATASET DE ADMISIÓN ---")

        nulos_admision = (
            self.df_admision
            .isnull()
            .sum()
        )

        nulos_admision = (
            nulos_admision[
                nulos_admision > 0
            ]
        )

        if len(nulos_admision) == 0:
            print("No existen valores nulos.")
        else:
            print(nulos_admision)

    # ==========================================================
    # DUPLICADOS
    # ==========================================================

    def analizar_duplicados(self):
        """
        Analiza duplicados exactos sin eliminarlos.
        """

        print("\n========================================")
        print("ANÁLISIS DE DUPLICADOS")
        print("========================================")

        duplicados_matricula = (
            self.df_matricula
            .duplicated()
            .sum()
        )

        duplicados_admision = (
            self.df_admision
            .duplicated()
            .sum()
        )

        print("\nDataset de matrícula:")

        print(
            f"Duplicados exactos: "
            f"{duplicados_matricula}"
        )

        print("\nDataset de admisión:")

        print(
            f"Duplicados exactos: "
            f"{duplicados_admision}"
        )

        print(
            "\nLos datasets NO fueron modificados."
        )

    # ==========================================================
    # ESTADÍSTICA DESCRIPTIVA
    # ==========================================================

    def estadistica_descriptiva(self):
        """
        Genera estadísticas descriptivas para las variables
        numéricas disponibles.
        """

        print("\n========================================")
        print("ESTADÍSTICA DESCRIPTIVA")
        print("========================================")

        # ------------------------------------------------------
        # MATRÍCULA
        # ------------------------------------------------------

        print("\n--- DATASET DE MATRÍCULA ---")

        columnas_numericas = (
            self.df_matricula
            .select_dtypes(
                include=["number"]
            )
            .columns
        )

        if len(columnas_numericas) == 0:

            print(
                "No existen variables numéricas."
            )

        else:

            print(
                "\nVariables numéricas:"
            )

            for columna in columnas_numericas:
                print(f"- {columna}")

            print(
                "\nResumen estadístico:"
            )

            print(
                self.df_matricula[
                    columnas_numericas
                ].describe()
            )

        # ------------------------------------------------------
        # ADMISIÓN
        # ------------------------------------------------------

        print("\n--- DATASET DE ADMISIÓN ---")

        columnas_numericas = (
            self.df_admision
            .select_dtypes(
                include=["number"]
            )
            .columns
        )

        if len(columnas_numericas) == 0:

            print(
                "No existen variables numéricas."
            )

        else:

            print(
                "\nVariables numéricas:"
            )

            for columna in columnas_numericas:
                print(f"- {columna}")

            print(
                "\nResumen estadístico:"
            )

            print(
                self.df_admision[
                    columnas_numericas
                ].describe()
            )

    # ==========================================================
    # ANÁLISIS DE EDAD
    # ==========================================================

    def analizar_edad_matricula(self):
        """
        Analiza la distribución de EDAD en el dataset
        de matrícula.
        """

        print("\n========================================")
        print("ANÁLISIS DE EDAD - MATRÍCULA")
        print("========================================")

        if "EDAD" not in self.df_matricula.columns:

            print(
                "La columna EDAD no existe."
            )

            return

        edad = self.df_matricula["EDAD"]

        print(
            f"Valores nulos: "
            f"{edad.isnull().sum()}"
        )

        print(
            f"Edad mínima: "
            f"{edad.min()}"
        )

        print(
            f"Edad máxima: "
            f"{edad.max()}"
        )

        print(
            f"Edad promedio: "
            f"{edad.mean():.2f}"
        )

        print(
            f"Mediana: "
            f"{edad.median():.2f}"
        )

        print(
            f"Desviación estándar: "
            f"{edad.std():.2f}"
        )

        print("\nFrecuencia de edades:")

        print(
            edad.value_counts()
            .sort_index()
        )

    # ==========================================================
    # ANÁLISIS DE VARIABLES CATEGÓRICAS
    # ==========================================================

    def analizar_categorias(self, limite=10):
        """
        Analiza las categorías principales de variables
        categóricas seleccionadas.
        """

        print("\n========================================")
        print("ANÁLISIS DE VARIABLES CATEGÓRICAS")
        print("========================================")

        columnas_matricula = [
            "AÑO",
            "UNIVERSIDAD",
            "TIPO_MATRICULA",
            "CARRERA",
            "GRADO_ACADEMICO",
            "NIVEL_ACADEMICO",
            "AREA_CONOCIMIENTO",
            "STEM_MICITT",
            "SEXO",
            "PROVINCIA_ESTUDIANTE",
            "REGION_PLANIFICACION_ESTUDIANTE",
            "GAM_ESTUDIANTE",
            "TIPO_NACIONALIDAD"
        ]

        print("\n--- DATASET DE MATRÍCULA ---")

        for columna in columnas_matricula:

            if columna not in self.df_matricula.columns:
                continue

            print("\n----------------------------------------")
            print(f"COLUMNA: {columna}")
            print("----------------------------------------")

            print(
                f"Valores únicos: "
                f"{self.df_matricula[columna].nunique()}"
            )

            print("\nValores más frecuentes:")

            print(
                self.df_matricula[columna]
                .value_counts(
                    dropna=False
                )
                .head(limite)
            )

        columnas_admision = [
            "ANO_CONCURSO",
            "SEXO",
            "NACIONALIDAD",
            "RANGO_EDAD",
            "PROVINCIA_RESIDENCIA",
            "SEDE",
            "RECINTO",
            "RANGO_NOTA_ADMISION",
            "TIPO_COLEGIO",
            "TIPO_HORARIO_COLEGIO",
            "TIPO_MODALIDAD_COLEGIO",
            "TIPO_PROCESO_ADMISION",
            "CARRERA"
        ]

        print("\n--- DATASET DE ADMISIÓN ---")

        for columna in columnas_admision:

            if columna not in self.df_admision.columns:
                continue

            print("\n----------------------------------------")
            print(f"COLUMNA: {columna}")
            print("----------------------------------------")

            print(
                f"Valores únicos: "
                f"{self.df_admision[columna].nunique()}"
            )

            print("\nValores más frecuentes:")

            print(
                self.df_admision[columna]
                .value_counts(
                    dropna=False
                )
                .head(limite)
            )

    # ==========================================================
    # ANÁLISIS TEMPORAL
    # ==========================================================

    def analizar_periodo(self):
        """
        Analiza la distribución temporal de ambos datasets.
        """

        print("\n========================================")
        print("ANÁLISIS TEMPORAL")
        print("========================================")

        print("\n--- MATRÍCULA ---")

        if "AÑO" in self.df_matricula.columns:

            print(
                self.df_matricula["AÑO"]
                .value_counts()
                .sort_index()
            )

        print("\n--- ADMISIÓN ---")

        if "ANO_CONCURSO" in self.df_admision.columns:

            print(
                self.df_admision["ANO_CONCURSO"]
                .value_counts()
                .sort_index()
            )

    # ==========================================================
    # ANÁLISIS DE MATRÍCULA POR UNIVERSIDAD
    # ==========================================================

    def analizar_universidades(self):
        """
        Analiza la cantidad de registros de matrícula
        por universidad.
        """

        print("\n========================================")
        print("ANÁLISIS POR UNIVERSIDAD")
        print("========================================")

        if "UNIVERSIDAD" not in self.df_matricula.columns:
            print(
                "La columna UNIVERSIDAD no existe."
            )
            return

        conteo = (
            self.df_matricula[
                "UNIVERSIDAD"
            ]
            .value_counts()
        )

        print("\nMatrícula por universidad:")

        print(conteo)

        porcentaje = (
            conteo
            / len(self.df_matricula)
            * 100
        )

        resultado = pd.DataFrame({
            "REGISTROS": conteo,
            "PORCENTAJE": porcentaje.round(2)
        })

        print(
            "\nParticipación porcentual:"
        )

        print(resultado)

    # ==========================================================
    # ANÁLISIS DE TIPO DE MATRÍCULA
    # ==========================================================

    def analizar_tipo_matricula(self):
        """
        Analiza la distribución entre primer ingreso
        y no primer ingreso.
        """

        print("\n========================================")
        print("ANÁLISIS DE TIPO DE MATRÍCULA")
        print("========================================")

        if "TIPO_MATRICULA" not in self.df_matricula.columns:
            print(
                "La columna TIPO_MATRICULA no existe."
            )
            return

        conteo = (
            self.df_matricula[
                "TIPO_MATRICULA"
            ]
            .value_counts()
        )

        porcentaje = (
            conteo
            / len(self.df_matricula)
            * 100
        )

        resultado = pd.DataFrame({
            "REGISTROS": conteo,
            "PORCENTAJE": porcentaje.round(2)
        })

        print(resultado)

    # ==========================================================
    # ANÁLISIS DE STEM
    # ==========================================================

    def analizar_stem(self):
        """
        Analiza la distribución de carreras STEM y NO STEM.
        """

        print("\n========================================")
        print("ANÁLISIS STEM")
        print("========================================")

        if "STEM_MICITT" not in self.df_matricula.columns:

            print(
                "La columna STEM_MICITT no existe."
            )

            return

        conteo = (
            self.df_matricula[
                "STEM_MICITT"
            ]
            .value_counts()
        )

        porcentaje = (
            conteo
            / len(self.df_matricula)
            * 100
        )

        resultado = pd.DataFrame({
            "REGISTROS": conteo,
            "PORCENTAJE": porcentaje.round(2)
        })

        print(resultado)

    # ==========================================================
    # ANÁLISIS POR SEXO
    # ==========================================================

    def analizar_sexo(self):
        """
        Analiza la distribución por sexo en ambos datasets.
        """

        print("\n========================================")
        print("ANÁLISIS POR SEXO")
        print("========================================")

        print("\n--- MATRÍCULA ---")

        if "SEXO" in self.df_matricula.columns:

            print(
                self.df_matricula[
                    "SEXO"
                ]
                .value_counts(
                    dropna=False
                )
            )

        print("\n--- ADMISIÓN ---")

        if "SEXO" in self.df_admision.columns:

            print(
                self.df_admision[
                    "SEXO"
                ]
                .value_counts(
                    dropna=False
                )
            )

    # ==========================================================
    # ANÁLISIS GEOGRÁFICO
    # ==========================================================

    def analizar_geografia(self):
        """
        Analiza las principales variables geográficas
        disponibles.
        """

        print("\n========================================")
        print("ANÁLISIS GEOGRÁFICO")
        print("========================================")

        print("\n--- MATRÍCULA: PROVINCIA ---")

        if (
            "PROVINCIA_ESTUDIANTE"
            in self.df_matricula.columns
        ):

            print(
                self.df_matricula[
                    "PROVINCIA_ESTUDIANTE"
                ]
                .value_counts(
                    dropna=False
                )
            )

        print("\n--- MATRÍCULA: GAM ---")

        if "GAM_ESTUDIANTE" in self.df_matricula.columns:

            print(
                self.df_matricula[
                    "GAM_ESTUDIANTE"
                ]
                .value_counts(
                    dropna=False
                )
            )

        print("\n--- ADMISIÓN: PROVINCIA ---")

        if (
            "PROVINCIA_RESIDENCIA"
            in self.df_admision.columns
        ):

            print(
                self.df_admision[
                    "PROVINCIA_RESIDENCIA"
                ]
                .value_counts(
                    dropna=False
                )
            )

    # ==========================================================
    # ANÁLISIS DEL DATASET DE ADMISIÓN
    # ==========================================================

    def analizar_admision(self):
        """
        Analiza variables relevantes del proceso de admisión.
        """

        print("\n========================================")
        print("ANÁLISIS DEL DATASET DE ADMISIÓN")
        print("========================================")

        columnas = [
            "RANGO_EDAD",
            "RANGO_NOTA_ADMISION",
            "TIPO_COLEGIO",
            "TIPO_HORARIO_COLEGIO",
            "TIPO_MODALIDAD_COLEGIO",
            "TIPO_PROCESO_ADMISION"
        ]

        for columna in columnas:

            if columna not in self.df_admision.columns:
                continue

            print("\n----------------------------------------")
            print(f"{columna}")
            print("----------------------------------------")

            conteo = (
                self.df_admision[
                    columna
                ]
                .value_counts(
                    dropna=False
                )
            )

            porcentaje = (
                conteo
                / len(self.df_admision)
                * 100
            )

            resultado = pd.DataFrame({
                "REGISTROS": conteo,
                "PORCENTAJE": porcentaje.round(2)
            })

            print(resultado)

    # ==========================================================
    # RESUMEN DEL EDA
    # ==========================================================

    def resumen(self):
        """
        Presenta un resumen general de ambos datasets.
        """

        print("\n========================================")
        print("RESUMEN DEL EDA")
        print("========================================")

        print("\nDataset de matrícula:")

        print(
            f"- Registros: "
            f"{len(self.df_matricula)}"
        )

        print(
            f"- Variables: "
            f"{len(self.df_matricula.columns)}"
        )

        print(
            f"- Duplicados exactos: "
            f"{self.df_matricula.duplicated().sum()}"
        )

        print(
            f"- Valores nulos totales: "
            f"{self.df_matricula.isnull().sum().sum()}"
        )

        print("\nDataset de admisión:")

        print(
            f"- Registros: "
            f"{len(self.df_admision)}"
        )

        print(
            f"- Variables: "
            f"{len(self.df_admision.columns)}"
        )

        print(
            f"- Duplicados exactos: "
            f"{self.df_admision.duplicated().sum()}"
        )

        print(
            f"- Valores nulos totales: "
            f"{self.df_admision.isnull().sum().sum()}"
        )

        print(
            "\nEDA analítico completado."
        )

        print(
            "Los datasets procesados "
            "no fueron modificados."
        )