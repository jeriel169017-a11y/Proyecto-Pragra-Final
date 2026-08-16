import os

from src.eda.procesador_eda import ProcesadorEDA
from src.visualizacion.visualizador import Visualizador
from src.basedatos.gestor_base_datos import GestorBaseDatos
from src.analisis.analizador_academico import AnalizadorAcademico

from cargar_datos_sql import cargar_datasets_sql


def main():

    print("\n")
    print("========================================")
    print("PROYECTO DE DESERCIÓN ESTUDIANTIL")
    print("========================================")

    # ==========================================================
    # RUTAS DEL PROYECTO
    # ==========================================================

    ruta_matricula = os.path.join(
        "data",
        "processed",
        "conare_matricula_limpio.csv"
    )

    ruta_admision = os.path.join(
        "data",
        "processed",
        "conare_admision_limpio.csv"
    )

    ruta_graficos = os.path.join(
        "data",
        "resultados",
        "graficos"
    )

    # Crear carpeta de gráficos si no existe
    os.makedirs(
        ruta_graficos,
        exist_ok=True
    )

    # ==========================================================
    # ETAPA 1 - ANÁLISIS EXPLORATORIO
    # ==========================================================

    print("\n")
    print("========================================")
    print("ETAPA 1 - ANÁLISIS EXPLORATORIO")
    print("========================================")

    eda = ProcesadorEDA(
        ruta_matricula=ruta_matricula,
        ruta_admision=ruta_admision
    )

    eda.cargar_datasets()

    eda.informacion_general()

    eda.analizar_nulos()

    eda.analizar_duplicados()

    eda.estadistica_descriptiva()

    eda.analizar_edad_matricula()

    eda.analizar_categorias()

    eda.analizar_periodo()

    eda.analizar_universidades()

    eda.analizar_tipo_matricula()

    eda.analizar_stem()

    eda.analizar_sexo()

    eda.analizar_geografia()

    eda.analizar_admision()

    eda.resumen()

    # ==========================================================
    # ETAPA 2 - VISUALIZACIÓN DEL EDA
    # ==========================================================

    print("\n")
    print("========================================")
    print("ETAPA 2 - VISUALIZACIÓN DEL EDA")
    print("========================================")

    visualizador = Visualizador(
        ruta_matricula=ruta_matricula,
        ruta_admision=ruta_admision,
        ruta_salida=ruta_graficos
    )

    visualizador.cargar_datasets()

    visualizador.generar_todas()

    # ==========================================================
    # ETAPA 3 - CARGA DE DATOS A SQL SERVER
    # ==========================================================

    print("\n")
    print("========================================")
    print("ETAPA 3 - CARGA DE DATOS A SQL SERVER")
    print("========================================")

    resultado_sql = cargar_datasets_sql()

    print("\n")
    print("========================================")
    print("RESUMEN DE CARGA SQL")
    print("========================================")

    print(
        resultado_sql.to_string(
            index=False
        )
    )

    # ==========================================================
    # ETAPA 4 - CONEXIÓN Y VERIFICACIÓN DE SQL SERVER
    # ==========================================================

    print("\n")
    print("========================================")
    print("ETAPA 4 - VERIFICACIÓN DE SQL SERVER")
    print("========================================")

    servidor = "localhost"
    base_datos = "DesercionEstudiantil"

    gestor_bd = GestorBaseDatos(
        servidor=servidor,
        base_datos=base_datos
    )

    try:

        gestor_bd.conectar()

        # ------------------------------------------------------
        # VER TABLAS DISPONIBLES
        # ------------------------------------------------------

        consulta_tablas = """

        SELECT
            TABLE_NAME
        FROM INFORMATION_SCHEMA.TABLES
        WHERE TABLE_TYPE = 'BASE TABLE';

        """

        tablas = gestor_bd.ejecutar_consulta(
            consulta_tablas
        )

        print("\nTablas disponibles en la base de datos:")

        print(
            tablas.to_string(
                index=False
            )
        )

        # ------------------------------------------------------
        # CONTAR CONARE_Matricula
        # ------------------------------------------------------

        consulta_matricula = """

        SELECT
            COUNT(*) AS TOTAL_REGISTROS
        FROM dbo.CONARE_Matricula;

        """

        cantidad_matricula = (
            gestor_bd.ejecutar_consulta(
                consulta_matricula
            )
        )

        print(
            "\nCantidad de registros en CONARE_Matricula:"
        )

        print(
            cantidad_matricula.to_string(
                index=False
            )
        )

        # ------------------------------------------------------
        # CONTAR CONARE_Admision
        # ------------------------------------------------------

        consulta_admision = """

        SELECT
            COUNT(*) AS TOTAL_REGISTROS
        FROM dbo.CONARE_Admision;

        """

        cantidad_admision = (
            gestor_bd.ejecutar_consulta(
                consulta_admision
            )
        )

        print(
            "\nCantidad de registros en CONARE_Admision:"
        )

        print(
            cantidad_admision.to_string(
                index=False
            )
        )

        # ------------------------------------------------------
        # MUESTRA MATRÍCULA
        # ------------------------------------------------------

        print("\n--- MUESTRA CONARE_Matricula ---")

        muestra_matricula = (
            gestor_bd.ejecutar_consulta(
                """
                SELECT TOP 5 *
                FROM dbo.CONARE_Matricula;
                """
            )
        )

        print(
            muestra_matricula.to_string(
                index=False
            )
        )

        # ------------------------------------------------------
        # MUESTRA ADMISIÓN
        # ------------------------------------------------------

        print("\n--- MUESTRA CONARE_Admision ---")

        muestra_admision = (
            gestor_bd.ejecutar_consulta(
                """
                SELECT TOP 5 *
                FROM dbo.CONARE_Admision;
                """
            )
        )

        print(
            muestra_admision.to_string(
                index=False
            )
        )

    finally:

        gestor_bd.cerrar_conexion()

    # ==========================================================
    # ETAPA 5 - ANÁLISIS ACADÉMICO
    # ==========================================================

    print("\n")
    print("========================================")
    print("ETAPA 5 - ANÁLISIS ACADÉMICO")
    print("========================================")

    print(
        "\nEl módulo AnalizadorAcademico existe en el proyecto."
    )

    print(
        "Se mantiene disponible para la siguiente etapa "
        "del análisis según las fuentes académicas definidas."
    )

    # ==========================================================
    # FINAL
    # ==========================================================

    print("\n")
    print("========================================")
    print("PROYECTO EJECUTADO CORRECTAMENTE")
    print("========================================")

    print("\nEtapas completadas:")

    print("1. Carga de datasets procesados")
    print("2. Análisis exploratorio de datos")
    print("3. Análisis estadístico")
    print("4. Análisis categórico")
    print("5. Análisis temporal")
    print("6. Análisis geográfico")
    print("7. Análisis de admisión")
    print("8. Generación de visualizaciones")
    print("9. Carga de matrícula a SQL Server")
    print("10. Carga de admisión a SQL Server")
    print("11. Verificación de registros en SQL Server")
    print("12. Verificación de datos cargados")

    print("\nLos gráficos se encuentran en:")
    print(ruta_graficos)

    print("\n========================================")


if __name__ == "__main__":
    main()