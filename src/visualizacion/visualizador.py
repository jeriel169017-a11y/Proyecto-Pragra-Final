import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


class Visualizador:
    """
    Clase encargada de generar las visualizaciones
    correspondientes al análisis exploratorio de datos (EDA).

    Características:
    - Utiliza únicamente los datasets procesados.
    - No modifica los datasets.
    - Guarda los gráficos en data/resultados/graficos.
    """

    def __init__(self, ruta_matricula, ruta_admision, ruta_salida):
        self.ruta_matricula = ruta_matricula
        self.ruta_admision = ruta_admision
        self.ruta_salida = ruta_salida

        self.df_matricula = None
        self.df_admision = None

        os.makedirs(self.ruta_salida, exist_ok=True)

        sns.set_theme(
            style="whitegrid",
            palette="deep"
        )

    # ==========================================================
    # CARGAR DATASETS
    # ==========================================================

    def cargar_datasets(self):
        """
        Carga los datasets procesados.
        """

        print("\n========================================")
        print("CARGANDO DATASETS PARA VISUALIZACIÓN")
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

        print(
            f"\nMatrícula: "
            f"{self.df_matricula.shape[0]} filas, "
            f"{self.df_matricula.shape[1]} columnas."
        )

        print(
            f"Admisión: "
            f"{self.df_admision.shape[0]} filas, "
            f"{self.df_admision.shape[1]} columnas."
        )

    # ==========================================================
    # UTILIDAD PARA GUARDAR GRÁFICOS
    # ==========================================================

    def guardar_grafico(self, nombre_archivo):
        """
        Guarda el gráfico actual en la carpeta de resultados.
        """

        ruta = os.path.join(
            self.ruta_salida,
            nombre_archivo
        )

        plt.tight_layout()
        plt.savefig(
            ruta,
            dpi=300,
            bbox_inches="tight"
        )

        plt.close()

        print(f"Gráfico generado: {ruta}")

    # ==========================================================
    # MATRÍCULA POR AÑO
    # ==========================================================

    def grafico_matricula_por_anio(self):
        """
        Muestra la cantidad de registros de matrícula
        por año.
        """

        datos = (
            self.df_matricula["AÑO"]
            .value_counts()
            .sort_index()
        )

        plt.figure(figsize=(10, 6))

        sns.barplot(
            x=datos.index.astype(str),
            y=datos.values,
            color="#2E86C1"
        )

        plt.title(
            "Matrícula por año"
        )

        plt.xlabel("Año")
        plt.ylabel("Cantidad de registros")

        self.guardar_grafico(
            "01_matricula_por_anio.png"
        )

    # ==========================================================
    # MATRÍCULA POR UNIVERSIDAD
    # ==========================================================

    def grafico_matricula_por_universidad(self):
        """
        Muestra la distribución de matrícula
        por universidad.
        """

        datos = (
            self.df_matricula["UNIVERSIDAD"]
            .value_counts()
            .sort_values()
        )

        plt.figure(figsize=(10, 6))

        sns.barplot(
            x=datos.values,
            y=datos.index,
            color="#2874A6"
        )

        plt.title(
            "Matrícula por universidad"
        )

        plt.xlabel("Cantidad de registros")
        plt.ylabel("Universidad")

        self.guardar_grafico(
            "02_matricula_por_universidad.png"
        )

    # ==========================================================
    # TIPO DE MATRÍCULA
    # ==========================================================

    def grafico_tipo_matricula(self):
        """
        Compara primer ingreso y no primer ingreso.
        """

        datos = (
            self.df_matricula["TIPO_MATRICULA"]
            .value_counts()
        )

        plt.figure(figsize=(8, 6))

        sns.barplot(
            x=datos.index,
            y=datos.values,
            color="#17A589"
        )

        plt.title(
            "Tipo de matrícula"
        )

        plt.xlabel("Tipo de matrícula")
        plt.ylabel("Cantidad de registros")

        plt.xticks(rotation=15)

        self.guardar_grafico(
            "03_tipo_matricula.png"
        )

    # ==========================================================
    # MATRÍCULA POR SEXO
    # ==========================================================

    def grafico_sexo_matricula(self):
        """
        Distribución de matrícula por sexo.
        """

        datos = (
            self.df_matricula["SEXO"]
            .value_counts()
        )

        plt.figure(figsize=(8, 6))

        sns.barplot(
            x=datos.index,
            y=datos.values,
            color="#8E44AD"
        )

        plt.title(
            "Matrícula por sexo"
        )

        plt.xlabel("Sexo")
        plt.ylabel("Cantidad de registros")

        self.guardar_grafico(
            "04_matricula_por_sexo.png"
        )

    # ==========================================================
    # STEM
    # ==========================================================

    def grafico_stem(self):
        """
        Distribución de matrícula entre STEM y no STEM.
        """

        datos = (
            self.df_matricula["STEM_MICITT"]
            .value_counts()
        )

        plt.figure(figsize=(8, 6))

        sns.barplot(
            x=datos.index,
            y=datos.values,
            color="#D35400"
        )

        plt.title(
            "Matrícula STEM vs. No STEM"
        )

        plt.xlabel("Clasificación")
        plt.ylabel("Cantidad de registros")

        self.guardar_grafico(
            "05_stem_vs_no_stem.png"
        )

    # ==========================================================
    # EDAD
    # ==========================================================

    def grafico_distribucion_edad(self):
        """
        Histograma de la distribución de edades.
        """

        plt.figure(figsize=(10, 6))

        sns.histplot(
            data=self.df_matricula,
            x="EDAD",
            bins=30,
            kde=True,
            color="#3498DB"
        )

        plt.title(
            "Distribución de edad de estudiantes"
        )

        plt.xlabel("Edad")
        plt.ylabel("Frecuencia")

        self.guardar_grafico(
            "06_distribucion_edad.png"
        )

    # ==========================================================
    # PROVINCIA
    # ==========================================================

    def grafico_provincia_matricula(self):
        """
        Distribución de matrícula por provincia.
        """

        datos = (
            self.df_matricula[
                "PROVINCIA_ESTUDIANTE"
            ]
            .value_counts()
            .sort_values()
        )

        plt.figure(figsize=(10, 7))

        sns.barplot(
            x=datos.values,
            y=datos.index,
            color="#229954"
        )

        plt.title(
            "Matrícula por provincia de residencia"
        )

        plt.xlabel("Cantidad de registros")
        plt.ylabel("Provincia")

        self.guardar_grafico(
            "07_matricula_por_provincia.png"
        )

    # ==========================================================
    # MATRÍCULA POR ÁREA DE CONOCIMIENTO
    # ==========================================================

    def grafico_area_conocimiento(self):
        """
        Distribución de matrícula por área de conocimiento.
        """

        datos = (
            self.df_matricula[
                "AREA_CONOCIMIENTO"
            ]
            .value_counts()
            .sort_values()
        )

        plt.figure(figsize=(10, 7))

        sns.barplot(
            x=datos.values,
            y=datos.index,
            color="#7D3C98"
        )

        plt.title(
            "Matrícula por área de conocimiento"
        )

        plt.xlabel("Cantidad de registros")
        plt.ylabel("Área de conocimiento")

        self.guardar_grafico(
            "08_area_conocimiento.png"
        )

    # ==========================================================
    # ADMISIÓN POR AÑO
    # ==========================================================

    def grafico_admision_por_anio(self):
        """
        Evolución de los registros de admisión por año.
        """

        datos = (
            self.df_admision["ANO_CONCURSO"]
            .value_counts()
            .sort_index()
        )

        plt.figure(figsize=(11, 6))

        sns.lineplot(
            x=datos.index,
            y=datos.values,
            marker="o",
            linewidth=2,
            color="#C0392B"
        )

        plt.title(
            "Evolución de registros de admisión"
        )

        plt.xlabel("Año de concurso")
        plt.ylabel("Cantidad de registros")

        self.guardar_grafico(
            "09_admision_por_anio.png"
        )

    # ==========================================================
    # RANGO DE EDAD DE ADMISIÓN
    # ==========================================================

    def grafico_rango_edad_admision(self):
        """
        Distribución de aspirantes según rango de edad.
        """

        datos = (
            self.df_admision["RANGO_EDAD"]
            .value_counts()
        )

        plt.figure(figsize=(9, 6))

        sns.barplot(
            x=datos.index,
            y=datos.values,
            color="#16A085"
        )

        plt.title(
            "Aspirantes por rango de edad"
        )

        plt.xlabel("Rango de edad")
        plt.ylabel("Cantidad de registros")

        plt.xticks(rotation=20)

        self.guardar_grafico(
            "10_rango_edad_admision.png"
        )

    # ==========================================================
    # NOTA DE ADMISIÓN
    # ==========================================================

    def grafico_nota_admision(self):
        """
        Distribución de los rangos de nota de admisión.
        """

        datos = (
            self.df_admision[
                "RANGO_NOTA_ADMISION"
            ]
            .value_counts()
        )

        plt.figure(figsize=(10, 6))

        sns.barplot(
            x=datos.index,
            y=datos.values,
            color="#F39C12"
        )

        plt.title(
            "Rango de nota de admisión"
        )

        plt.xlabel("Rango de nota")
        plt.ylabel("Cantidad de registros")

        plt.xticks(rotation=20)

        self.guardar_grafico(
            "11_rango_nota_admision.png"
        )

    # ==========================================================
    # TIPO DE COLEGIO
    # ==========================================================

    def grafico_tipo_colegio(self):
        """
        Distribución de aspirantes según tipo de colegio.
        """

        datos = (
            self.df_admision[
                "TIPO_COLEGIO"
            ]
            .value_counts()
            .sort_values()
        )

        plt.figure(figsize=(9, 6))

        sns.barplot(
            x=datos.values,
            y=datos.index,
            color="#5DADE2"
        )

        plt.title(
            "Aspirantes por tipo de colegio"
        )

        plt.xlabel("Cantidad de registros")
        plt.ylabel("Tipo de colegio")

        self.guardar_grafico(
            "12_tipo_colegio.png"
        )

    # ==========================================================
    # MODALIDAD DEL COLEGIO
    # ==========================================================

    def grafico_modalidad_colegio(self):
        """
        Distribución según modalidad del colegio.
        """

        datos = (
            self.df_admision[
                "TIPO_MODALIDAD_COLEGIO"
            ]
            .value_counts()
            .sort_values()
        )

        plt.figure(figsize=(9, 6))

        sns.barplot(
            x=datos.values,
            y=datos.index,
            color="#48C9B0"
        )

        plt.title(
            "Aspirantes por modalidad del colegio"
        )

        plt.xlabel("Cantidad de registros")
        plt.ylabel("Modalidad")

        self.guardar_grafico(
            "13_modalidad_colegio.png"
        )

    # ==========================================================
    # HORARIO DEL COLEGIO
    # ==========================================================

    def grafico_horario_colegio(self):
        """
        Distribución según horario del colegio.
        """

        datos = (
            self.df_admision[
                "TIPO_HORARIO_COLEGIO"
            ]
            .value_counts()
        )

        plt.figure(figsize=(9, 6))

        sns.barplot(
            x=datos.index,
            y=datos.values,
            color="#AF7AC5"
        )

        plt.title(
            "Aspirantes por horario del colegio"
        )

        plt.xlabel("Horario")
        plt.ylabel("Cantidad de registros")

        plt.xticks(rotation=15)

        self.guardar_grafico(
            "14_horario_colegio.png"
        )

    # ==========================================================
    # PROCESO DE ADMISIÓN
    # ==========================================================

    def grafico_proceso_admision(self):
        """
        Distribución según tipo de proceso de admisión.
        """

        datos = (
            self.df_admision[
                "TIPO_PROCESO_ADMISION"
            ]
            .value_counts()
        )

        plt.figure(figsize=(8, 6))

        sns.barplot(
            x=datos.index,
            y=datos.values,
            color="#E74C3C"
        )

        plt.title(
            "Tipo de proceso de admisión"
        )

        plt.xlabel("Tipo de proceso")
        plt.ylabel("Cantidad de registros")

        self.guardar_grafico(
            "15_proceso_admision.png"
        )

    # ==========================================================
    # ADMISIÓN POR SEXO
    # ==========================================================

    def grafico_sexo_admision(self):
        """
        Distribución de aspirantes por sexo.
        """

        datos = (
            self.df_admision["SEXO"]
            .value_counts()
        )

        plt.figure(figsize=(8, 6))

        sns.barplot(
            x=datos.index,
            y=datos.values,
            color="#5499C7"
        )

        plt.title(
            "Aspirantes por sexo"
        )

        plt.xlabel("Sexo")
        plt.ylabel("Cantidad de registros")

        self.guardar_grafico(
            "16_admision_por_sexo.png"
        )

    # ==========================================================
    # ADMISIÓN POR PROVINCIA
    # ==========================================================

    def grafico_provincia_admision(self):
        """
        Distribución de aspirantes por provincia de residencia.
        """

        datos = (
            self.df_admision[
                "PROVINCIA_RESIDENCIA"
            ]
            .value_counts()
            .sort_values()
        )

        plt.figure(figsize=(10, 7))

        sns.barplot(
            x=datos.values,
            y=datos.index,
            color="#1ABC9C"
        )

        plt.title(
            "Aspirantes por provincia de residencia"
        )

        plt.xlabel("Cantidad de registros")
        plt.ylabel("Provincia")

        self.guardar_grafico(
            "17_admision_por_provincia.png"
        )

    # ==========================================================
    # RELACIÓN SEXO - TIPO DE MATRÍCULA
    # ==========================================================

    def grafico_sexo_tipo_matricula(self):
        """
        Analiza la relación entre sexo y tipo de matrícula.
        """

        tabla = pd.crosstab(
            self.df_matricula["SEXO"],
            self.df_matricula["TIPO_MATRICULA"]
        )

        tabla.plot(
            kind="bar",
            figsize=(10, 6)
        )

        plt.title(
            "Tipo de matrícula según sexo"
        )

        plt.xlabel("Sexo")
        plt.ylabel("Cantidad de registros")

        plt.xticks(rotation=0)
        plt.legend(
            title="Tipo de matrícula"
        )

        self.guardar_grafico(
            "18_sexo_vs_tipo_matricula.png"
        )

    # ==========================================================
    # RELACIÓN STEM - SEXO
    # ==========================================================

    def grafico_stem_sexo(self):
        """
        Analiza la relación entre STEM y sexo.
        """

        tabla = pd.crosstab(
            self.df_matricula["SEXO"],
            self.df_matricula["STEM_MICITT"]
        )

        tabla.plot(
            kind="bar",
            figsize=(10, 6)
        )

        plt.title(
            "STEM según sexo"
        )

        plt.xlabel("Sexo")
        plt.ylabel("Cantidad de registros")

        plt.xticks(rotation=0)
        plt.legend(
            title="Clasificación STEM"
        )

        self.guardar_grafico(
            "19_stem_vs_sexo.png"
        )

    # ==========================================================
    # UNIVERSIDAD VS TIPO DE MATRÍCULA
    # ==========================================================

    def grafico_universidad_tipo_matricula(self):
        """
        Analiza el tipo de matrícula por universidad.
        """

        tabla = pd.crosstab(
            self.df_matricula["UNIVERSIDAD"],
            self.df_matricula["TIPO_MATRICULA"]
        )

        tabla.plot(
            kind="bar",
            figsize=(12, 7)
        )

        plt.title(
            "Tipo de matrícula según universidad"
        )

        plt.xlabel("Universidad")
        plt.ylabel("Cantidad de registros")

        plt.xticks(
            rotation=25,
            ha="right"
        )

        plt.legend(
            title="Tipo de matrícula"
        )

        self.guardar_grafico(
            "20_universidad_vs_tipo_matricula.png"
        )

    # ==========================================================
    # EJECUTAR TODAS LAS VISUALIZACIONES
    # ==========================================================

    def generar_todas(self):
        """
        Ejecuta todas las visualizaciones del EDA.
        """

        print("\n========================================")
        print("GENERANDO VISUALIZACIONES DEL EDA")
        print("========================================")

        self.grafico_matricula_por_anio()
        self.grafico_matricula_por_universidad()
        self.grafico_tipo_matricula()
        self.grafico_sexo_matricula()
        self.grafico_stem()
        self.grafico_distribucion_edad()
        self.grafico_provincia_matricula()
        self.grafico_area_conocimiento()

        self.grafico_admision_por_anio()
        self.grafico_rango_edad_admision()
        self.grafico_nota_admision()
        self.grafico_tipo_colegio()
        self.grafico_modalidad_colegio()
        self.grafico_horario_colegio()
        self.grafico_proceso_admision()
        self.grafico_sexo_admision()
        self.grafico_provincia_admision()

        self.grafico_sexo_tipo_matricula()
        self.grafico_stem_sexo()
        self.grafico_universidad_tipo_matricula()

        print("\n========================================")
        print("VISUALIZACIONES COMPLETADAS")
        print("========================================")

        print(
            f"\nLos gráficos fueron guardados en:\n"
            f"{self.ruta_salida}"
        )