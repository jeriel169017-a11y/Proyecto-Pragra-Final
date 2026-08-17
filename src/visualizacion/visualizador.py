import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# Clase encargada de generar las visualizaciones
# Características:
# Utiliza únicamente los datasets procesados
# No modifica los datasets
# Guarda los gráficos en data/resultados/graficos
class Visualizador:
    def __init__(self, ruta_matricula, ruta_admision, ruta_salida):
        self.ruta_matricula = ruta_matricula
        self.ruta_admision = ruta_admision
        self.ruta_salida = ruta_salida
        self.df_matricula = None
        self.df_admision = None
        os.makedirs(self.ruta_salida, exist_ok=True)
        sns.set_theme(style="whitegrid",palette="deep")
    # Cargar datasets
    def cargar_datasets(self):
        print("\n========================================")
        print("CARGANDO DATASETS PARA VISUALIZACIÓN")
        print("========================================")
        if not os.path.exists(self.ruta_matricula):
            raise FileNotFoundError(f"No se encontró el archivo de matrícula:\n"f"{self.ruta_matricula}")
        if not os.path.exists(self.ruta_admision):
            raise FileNotFoundError(f"No se encontró el archivo de admisión:\n"f"{self.ruta_admision}")
        self.df_matricula = pd.read_csv(self.ruta_matricula)
        self.df_admision = pd.read_csv(self.ruta_admision)
        print(f"\nMatrícula: "f"{self.df_matricula.shape[0]} filas, "f"{self.df_matricula.shape[1]} columnas.")
        print(f"Admisión: "f"{self.df_admision.shape[0]} filas, "f"{self.df_admision.shape[1]} columnas.")
    # Utilidad para guardar los resultados de los graficos
    def guardar_grafico(self, nombre_archivo):
        ruta = os.path.join(self.ruta_salida,nombre_archivo)
        plt.tight_layout()
        plt.savefig(ruta,dpi=300,bbox_inches="tight")
        plt.close()
        print(f"Gráfico generado: {ruta}")
    # Matricula por año
    # Muestra la cantidad de registros de matricula
    def grafico_matricula_por_anio(self):
        datos = (self.df_matricula["AÑO"].value_counts().sort_index())
        plt.figure(figsize=(10, 6))
        sns.barplot(x=datos.index.astype(str),y=datos.values,color="#2E86C1")
        plt.title("Matrícula por año")
        plt.xlabel("Año")
        plt.ylabel("Cantidad de registros")
        self.guardar_grafico("01_matricula_por_anio.png")
    # Matricula por universidad
    # Muestra la distribucion de matricula por universidad
    def grafico_matricula_por_universidad(self):
        datos = (self.df_matricula["UNIVERSIDAD"].value_counts().sort_values())
        plt.figure(figsize=(10, 6))
        sns.barplot(x=datos.values,y=datos.index,color="#2874A6")
        plt.title("Matrícula por universidad")
        plt.xlabel("Cantidad de registros")
        plt.ylabel("Universidad")
        self.guardar_grafico("02_matricula_por_universidad.png")
    # Tipo de matricula
    # Compara primer ingreso y no primer ingreso
    def grafico_tipo_matricula(self):
        datos = (self.df_matricula["TIPO_MATRICULA"].value_counts())
        plt.figure(figsize=(8, 6))
        sns.barplot(x=datos.index,y=datos.values,color="#17A589")
        plt.title("Tipo de matrícula")
        plt.xlabel("Tipo de matrícula")
        plt.ylabel("Cantidad de registros")
        plt.xticks(rotation=15)
        self.guardar_grafico("03_tipo_matricula.png")
    # Matricula por sexo
    # Distribucion de matricula por sexo
    def grafico_sexo_matricula(self):
        datos = (self.df_matricula["SEXO"].value_counts())
        plt.figure(figsize=(8, 6))
        sns.barplot(x=datos.index,y=datos.values,color="#8E44AD")
        plt.title("Matrícula por sexo")
        plt.xlabel("Sexo")
        plt.ylabel("Cantidad de registros")
        self.guardar_grafico("04_matricula_por_sexo.png")
    # STEM
    # Distribucion de matricula entre STEM y no STEM
    def grafico_stem(self):
        datos = (self.df_matricula["STEM_MICITT"].value_counts())
        plt.figure(figsize=(8, 6))
        sns.barplot(x=datos.index,y=datos.values,color="#D35400")
        plt.title("Matrícula STEM vs. No STEM")
        plt.xlabel("Clasificación")
        plt.ylabel("Cantidad de registros")
        self.guardar_grafico("05_stem_vs_no_stem.png")
    # Edad
    # Histograma de la distribucion de edades
    def grafico_distribucion_edad(self):
        plt.figure(figsize=(10, 6))
        sns.histplot(data=self.df_matricula,x="EDAD",bins=30,kde=True,color="#3498DB")
        plt.title("Distribución de edad de estudiantes")
        plt.xlabel("Edad")
        plt.ylabel("Frecuencia")
        self.guardar_grafico("06_distribucion_edad.png")
    # Provinvia
    # Distribucion de matricula por provincia
    def grafico_provincia_matricula(self):
        datos = (self.df_matricula["PROVINCIA_ESTUDIANTE"].value_counts().sort_values())
        plt.figure(figsize=(10, 7))
        sns.barplot(x=datos.values,y=datos.index,color="#229954")
        plt.title("Matrícula por provincia de residencia")
        plt.xlabel("Cantidad de registros")
        plt.ylabel("Provincia")
        self.guardar_grafico("07_matricula_por_provincia.png")
    # Matricula por area de conocimiento
    # Distribucion de matricula por area de conocimiento
    def grafico_area_conocimiento(self):
        datos = (self.df_matricula["AREA_CONOCIMIENTO"].value_counts().sort_values())
        plt.figure(figsize=(10, 7))
        sns.barplot(x=datos.values,y=datos.index,color="#7D3C98")
        plt.title("Matrícula por área de conocimiento")
        plt.xlabel("Cantidad de registros")
        plt.ylabel("Área de conocimiento")
        self.guardar_grafico("08_area_conocimiento.png")
    # Admision por año
    # Evolucion de los registros de admision por año
    def grafico_admision_por_anio(self):
        datos = (self.df_admision["ANO_CONCURSO"].value_counts().sort_index())
        plt.figure(figsize=(11, 6))
        sns.lineplot(x=datos.index,y=datos.values,marker="o",linewidth=2,color="#C0392B")
        plt.title("Evolución de registros de admisión")
        plt.xlabel("Año de concurso")
        plt.ylabel("Cantidad de registros")
        self.guardar_grafico("09_admision_por_anio.png")
    # Rango de edad de admision
    # Distribucion de aspirantes segun rango de edad
    def grafico_rango_edad_admision(self):
        datos = (self.df_admision["RANGO_EDAD"].value_counts())
        plt.figure(figsize=(9, 6))
        sns.barplot(x=datos.index,y=datos.values,color="#16A085")
        plt.title("Aspirantes por rango de edad")
        plt.xlabel("Rango de edad")
        plt.ylabel("Cantidad de registros")
        plt.xticks(rotation=20)
        self.guardar_grafico("10_rango_edad_admision.png")
    # Nota de admision
    # Distribucion de los rangos de nota de admision
    def grafico_nota_admision(self):
        datos = (self.df_admision["RANGO_NOTA_ADMISION"].value_counts())
        plt.figure(figsize=(10, 6))
        sns.barplot(x=datos.index,y=datos.values,color="#F39C12")
        plt.title("Rango de nota de admisión")
        plt.xlabel("Rango de nota")
        plt.ylabel("Cantidad de registros")
        plt.xticks(rotation=20)
        self.guardar_grafico("11_rango_nota_admision.png")
    # Tipo de colegio
    # Distribucion de aspirantes segun tipo de colegio
    def grafico_tipo_colegio(self):
        datos = (self.df_admision["TIPO_COLEGIO"].value_counts().sort_values())
        plt.figure(figsize=(9, 6))
        sns.barplot(x=datos.values,y=datos.index,color="#5DADE2")
        plt.title("Aspirantes por tipo de colegio")
        plt.xlabel("Cantidad de registros")
        plt.ylabel("Tipo de colegio")
        self.guardar_grafico("12_tipo_colegio.png")
    # Modalidad del colegio
    # Distribucion segun modalidad del colegio
    def grafico_modalidad_colegio(self):
        datos = (self.df_admision["TIPO_MODALIDAD_COLEGIO"].value_counts().sort_values())
        plt.figure(figsize=(9, 6))
        sns.barplot(x=datos.values,y=datos.index,color="#48C9B0")
        plt.title("Aspirantes por modalidad del colegio")
        plt.xlabel("Cantidad de registros")
        plt.ylabel("Modalidad")
        self.guardar_grafico("13_modalidad_colegio.png")
    # Horario del colegio
    # Distribucion seegun horario del colegio
    def grafico_horario_colegio(self):
        datos = (self.df_admision["TIPO_HORARIO_COLEGIO"].value_counts())
        plt.figure(figsize=(9, 6))
        sns.barplot(x=datos.index,y=datos.values,color="#AF7AC5")
        plt.title("Aspirantes por horario del colegio")
        plt.xlabel("Horario")
        plt.ylabel("Cantidad de registros")
        plt.xticks(rotation=15)
        self.guardar_grafico("14_horario_colegio.png")
    # Proceso de admision
    # Distribucion segun tipo de proceso de admision
    def grafico_proceso_admision(self):
        datos = (self.df_admision["TIPO_PROCESO_ADMISION"].value_counts())
        plt.figure(figsize=(8, 6))
        sns.barplot(x=datos.index,y=datos.values,color="#E74C3C")
        plt.title("Tipo de proceso de admisión")
        plt.xlabel("Tipo de proceso")
        plt.ylabel("Cantidad de registros")
        self.guardar_grafico("15_proceso_admision.png")
    # Admision por sexo
    # Distribucion de aspirantes por sexo
    def grafico_sexo_admision(self):
        datos = (self.df_admision["SEXO"].value_counts())
        plt.figure(figsize=(8, 6))
        sns.barplot(x=datos.index,y=datos.values,color="#5499C7")
        plt.title("Aspirantes por sexo")
        plt.xlabel("Sexo")
        plt.ylabel("Cantidad de registros")
        self.guardar_grafico("16_admision_por_sexo.png")
    # Admision por provincia
    # Distribucion de aspirantes por provincia de residencia
    def grafico_provincia_admision(self):
        datos = (self.df_admision["PROVINCIA_RESIDENCIA"].value_counts().sort_values())
        plt.figure(figsize=(10, 7))
        sns.barplot(x=datos.values,y=datos.index,color="#1ABC9C")
        plt.title("Aspirantes por provincia de residencia")
        plt.xlabel("Cantidad de registros")
        plt.ylabel("Provincia")
        self.guardar_grafico("17_admision_por_provincia.png")
    # Relacion sexo - Tipo de matrciula
    # Analiza la relacion entre sexo y tipo de matricula
    def grafico_sexo_tipo_matricula(self):
        tabla = pd.crosstab(self.df_matricula["SEXO"],self.df_matricula["TIPO_MATRICULA"])
        tabla.plot(kind="bar",figsize=(10, 6))
        plt.title("Tipo de matrícula según sexo")
        plt.xlabel("Sexo")
        plt.ylabel("Cantidad de registros")
        plt.xticks(rotation=0)
        plt.legend(title="Tipo de matrícula")
        self.guardar_grafico("18_sexo_vs_tipo_matricula.png")
    # Relacion STEM - Sexo
    # Analiza la relacion entre STEM y sexo
    def grafico_stem_sexo(self):
        tabla = pd.crosstab(self.df_matricula["SEXO"],self.df_matricula["STEM_MICITT"])
        tabla.plot(kind="bar",figsize=(10, 6))
        plt.title("STEM según sexo")
        plt.xlabel("Sexo")
        plt.ylabel("Cantidad de registros")
        plt.xticks(rotation=0)
        plt.legend(title="Clasificación STEM")
        self.guardar_grafico("19_stem_vs_sexo.png")
    # Universidad VS Tipo de matricula
    # Analiza el tipo de matricula por universidad
    def grafico_universidad_tipo_matricula(self):
        tabla = pd.crosstab(self.df_matricula["UNIVERSIDAD"],self.df_matricula["TIPO_MATRICULA"])
        tabla.plot(kind="bar",figsize=(12, 7))
        plt.title("Tipo de matrícula según universidad")
        plt.xlabel("Universidad")
        plt.ylabel("Cantidad de registros")
        plt.xticks(rotation=25,ha="right")
        plt.legend(title="Tipo de matrícula")
        self.guardar_grafico("20_universidad_vs_tipo_matricula.png")
    # Ejecutar todas las visualizaciones
    def generar_todas(self):
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
        print(f"\nLos gráficos fueron guardados en:\n"f"{self.ruta_salida}")