import os
import pandas as pd
class AnalizadorAcademico:
    def __init__(self, gestor_bd):
        self.gestor_bd = gestor_bd
        self.df = None
    # Cargar Datos
    def cargar_datos(self):
        print("\n")
        print("========================================")
        print("CARGANDO HISTORIAL ACADÉMICO")
        print("========================================")
        consulta = """
        SELECT
            ID_ESTUDIANTE,
            CARRERA,
            SEMESTRE,
            MATERIA,
            NOTA,
            CREDITOS_MATRICULADOS,
            CREDITOS_APROBADOS,
            CREDITOS_REPROBADOS,
            ASISTENCIA,
            PROMEDIO_SEMESTRE,
            PROMEDIO_ACUMULADO
        FROM HistorialAcademico;
        """
        self.df = self.gestor_bd.ejecutar_consulta(
            consulta)
        if self.df is None or self.df.empty:
            print("No existen datos en HistorialAcademico.")
            return False
        print(f"Registros cargados: "f"{len(self.df)}")
        print(f"Estudiantes: "f"{self.df['ID_ESTUDIANTE'].nunique()}")
        return True
    # Informacion General
    def informacion_general(self):
        if self.df is None:
            return
        print("\n")
        print("========================================")
        print("INFORMACIÓN DEL HISTORIAL ACADÉMICO")
        print("========================================")
        print(f"Registros: "f"{len(self.df)}")
        print(f"Estudiantes únicos: "f"{self.df['ID_ESTUDIANTE'].nunique()}")
        print("\nColumnas:")
        for columna in self.df.columns:
            print(f"- {columna}")
    # Analisis de notas
    def analizar_notas(self):
        print("\n")
        print("========================================")
        print("ANÁLISIS DE NOTAS")
        print("========================================")
        promedio = self.df["NOTA"].mean()
        minimo = self.df["NOTA"].min()
        maximo = self.df["NOTA"].max()
        print(f"Nota promedio: "f"{promedio:.2f}")
        print(f"Nota mínima: "f"{minimo:.2f}")
        print(f"Nota máxima: "f"{maximo:.2f}")
    # Analisis de creditos
    def analizar_creditos(self):
        print("\n")
        print("========================================")
        print("ANÁLISIS DE CRÉDITOS")
        print("========================================")
        matriculados = self.df["CREDITOS_MATRICULADOS"].sum()
        aprobados = self.df["CREDITOS_APROBADOS"].sum()
        reprobados = self.df["CREDITOS_REPROBADOS"].sum()
        print(f"Créditos matriculados: "f"{matriculados}")
        print(f"Créditos aprobados: "f"{aprobados}")
        print(f"Créditos reprobados: "f"{reprobados}")
        if matriculados > 0:
            porcentaje = (aprobados/ matriculados) * 100
            print(f"Porcentaje de aprobación: "f"{porcentaje:.2f}%")
    # Analisis de asistencia
    def analizar_asistencia(self):
        print("\n")
        print("========================================")
        print("ANÁLISIS DE ASISTENCIA")
        print("========================================")
        promedio = self.df["ASISTENCIA"].mean()
        print(f"Asistencia promedio: "f"{promedio:.2f}%")
    # Analisis de promedios
    def analizar_promedios(self):
        print("\n")
        print("========================================")
        print("ANÁLISIS DE PROMEDIOS")
        print("========================================")
        promedio_semestre = self.df["PROMEDIO_SEMESTRE"].mean()
        promedio_acumulado = self.df["PROMEDIO_ACUMULADO"].mean()
        print(f"Promedio semestral: "f"{promedio_semestre:.2f}")
        print(f"Promedio acumulado: "f"{promedio_acumulado:.2f}")
    # Indicadores por estudiante
    def indicadores_por_estudiante(self):
        print("\n")
        print("========================================")
        print("INDICADORES POR ESTUDIANTE")
        print("========================================")
        indicadores = (self.df.groupby("ID_ESTUDIANTE").agg(MATERIAS=("MATERIA","count"),
                NOTA_PROMEDIO=("NOTA","mean"),
                CREDITOS_MATRICULADOS=("CREDITOS_MATRICULADOS","sum"),
                CREDITOS_APROBADOS=("CREDITOS_APROBADOS","sum"),
                CREDITOS_REPROBADOS=("CREDITOS_REPROBADOS","sum"),
                ASISTENCIA_PROMEDIO=("ASISTENCIA","mean"),
                PROMEDIO_ACUMULADO=("PROMEDIO_ACUMULADO","last"),
                SEMESTRES=("SEMESTRE","nunique")).reset_index())
        # Porcentaje de aprobacion
        indicadores["PORCENTAJE_APROBACION"] = (indicadores["CREDITOS_APROBADOS"]/
            indicadores["CREDITOS_MATRICULADOS"]* 100)
        indicadores["PORCENTAJE_APROBACION"] = (indicadores["PORCENTAJE_APROBACION"].fillna(0))
        print(indicadores)
        return indicadores
    # Riesgo academico
    def analizar_riesgo_academico(
        self,
        indicadores
    ):
        print("\n")
        print("========================================")
        print("ANÁLISIS DE RIESGO ACADÉMICO")
        print("========================================")
        def determinar_riesgo(fila):
            nota = fila["NOTA_PROMEDIO"]
            aprobacion = fila["PORCENTAJE_APROBACION"]
            asistencia = fila["ASISTENCIA_PROMEDIO"]
            if (nota < 65
                or aprobacion < 70
                or asistencia < 70
            ):
                return "ALTO"
            elif (nota < 75
                or aprobacion < 85
                or asistencia < 80
            ):
                return "MEDIO"
            else:
                return "BAJO"
        indicadores["RIESGO_ACADEMICO"] = indicadores.apply(determinar_riesgo,axis=1)
        columnas_mostrar = ["ID_ESTUDIANTE","NOTA_PROMEDIO","ASISTENCIA_PROMEDIO","PORCENTAJE_APROBACION",
            "RIESGO_ACADEMICO"]
        print(indicadores[columnas_mostrar])
        return indicadores
    # Puntaje de riesgo de desercion
    def calcular_riesgo_desercion(
        self,
        indicadores
    ):
        print("\n")
        print("========================================")
        print("ANÁLISIS DE RIESGO DE DESERCIÓN")
        print("========================================")
        # Inicializar puntaje
        indicadores["PUNTAJE_RIESGO"] = 0
        # Nota promedio
        indicadores.loc[indicadores["NOTA_PROMEDIO"] < 65,"PUNTAJE_RIESGO"] += 2
        indicadores.loc[((indicadores["NOTA_PROMEDIO"] >= 65) & (indicadores["NOTA_PROMEDIO"] < 75)),
        "PUNTAJE_RIESGO"] += 1
        # Aprobacion
        indicadores.loc[indicadores["PORCENTAJE_APROBACION"] < 70,"PUNTAJE_RIESGO"] += 2
        indicadores.loc[((indicadores["PORCENTAJE_APROBACION"] >= 70) & (indicadores["PORCENTAJE_APROBACION"] < 85)),
        "PUNTAJE_RIESGO"] += 1
        # Asistencia
        indicadores.loc[indicadores["ASISTENCIA_PROMEDIO"] < 70,"PUNTAJE_RIESGO"] += 2
        indicadores.loc[((indicadores["ASISTENCIA_PROMEDIO"] >= 70) & (indicadores["ASISTENCIA_PROMEDIO"] < 80)),
        "PUNTAJE_RIESGO"] += 1
        # Creditos reprobados
        indicadores.loc[indicadores["CREDITOS_REPROBADOS"] > 6,"PUNTAJE_RIESGO"] += 1
        # Clasificacion final
        def clasificar_riesgo(puntaje):
            if puntaje >= 4:
                return "ALTO"
            elif puntaje >= 2:
                return "MEDIO"
            else:
                return "BAJO"
        indicadores["RIESGO_DESERCION"] = indicadores["PUNTAJE_RIESGO"].apply(clasificar_riesgo)
        # Mostrar resultados
        columnas = ["ID_ESTUDIANTE","NOTA_PROMEDIO","PORCENTAJE_APROBACION","ASISTENCIA_PROMEDIO","CREDITOS_REPROBADOS",
            "PUNTAJE_RIESGO","RIESGO_DESERCION"]
        print(indicadores[columnas])
        # Resumen de riesgo
        print("\n")
        print("DISTRIBUCIÓN DEL RIESGO:")
        distribucion = (indicadores["RIESGO_DESERCION"].value_counts())
        print(distribucion)
        return indicadores
    # Guardar indicadores
    def guardar_indicadores(
        self,
        indicadores
    ):
        print("\n")
        print("========================================")
        print("GUARDANDO INDICADORES ACADÉMICOS")
        print("========================================")
        # Crear carpeta de resultados
        carpeta_resultados = os.path.join("data","resultados","analisis_academico")
        os.makedirs(carpeta_resultados,exist_ok=True)
        # Ruta del archivo
        ruta_archivo = os.path.join(carpeta_resultados,"indicadores_academicos.csv")
        # Guardar DataFrame
        indicadores.to_csv(ruta_archivo,index=False,encoding="utf-8-sig")
        print("Indicadores guardados correctamente.")
        print(f"Archivo: {ruta_archivo}")
        print(f"Registros guardados: "f"{len(indicadores)}")
        return ruta_archivo
    # Ejecitar analisis completo
    def ejecutar(self):
        # Cargar datos
        if not self.cargar_datos():
            return None
        # Información general
        self.informacion_general()
        # Notas
        self.analizar_notas()
        # Créditos
        self.analizar_creditos()
        # Asistencia
        self.analizar_asistencia()
        # Promedios
        self.analizar_promedios()
        # Indicadores
        indicadores = (self.indicadores_por_estudiante())
        # Riesgo académico
        indicadores = (self.analizar_riesgo_academico(indicadores))
        # Riesgo de deserción
        indicadores = (self.calcular_riesgo_desercion(indicadores))
        # Guardar resultados
        self.guardar_indicadores(indicadores)
        # Mostrar resultado final
        print("\n")
        print("========================================")
        print("INDICADORES ACADÉMICOS GENERADOS")
        print("========================================")
        print(indicadores)
        # Resultado final
        return indicadores