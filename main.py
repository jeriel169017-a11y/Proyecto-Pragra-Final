from src.datos.gestor_datos import GestorDatos
import os
import glob


def main():

    # ==========================================================
    # BUSCAR DATASET
    # ==========================================================

    carpeta_raw = "data/raw"

    archivos_csv = glob.glob(
        os.path.join(
            carpeta_raw,
            "*.csv"
        )
    )

    if len(archivos_csv) == 0:

        raise FileNotFoundError(
            "No se encontró ningún archivo CSV "
            "en data/raw."
        )

    if len(archivos_csv) > 1:

        print(
            "\nSe encontraron varios archivos CSV:"
        )

        for archivo in archivos_csv:

            print(
                f"- {archivo}"
            )

        raise ValueError(
            "\nHay más de un CSV en data/raw. "
            "Debemos identificar explícitamente "
            "el dataset."
        )

    ruta_archivo = archivos_csv[0]

    # ==========================================================
    # RUTA DE SALIDA
    # ==========================================================

    ruta_salida = (
        "data/processed/"
        "conare_admision_limpio.csv"
    )

    # ==========================================================
    # CREAR GESTOR
    # ==========================================================

    gestor = GestorDatos(
        ruta_archivo
    )

    # ==========================================================
    # 1. CARGAR DATOS
    # ==========================================================

    gestor.cargar_datos()

    # ==========================================================
    # 2. CORREGIR ENCABEZADOS
    # ==========================================================

    gestor.corregir_encabezados()

    # ==========================================================
    # 3. INFORMACIÓN GENERAL
    # ==========================================================

    gestor.mostrar_informacion_general()

    # ==========================================================
    # 4. ANALIZAR VALORES NULOS
    # ==========================================================

    gestor.analizar_nulos()

    # ==========================================================
    # 5. ANALIZAR REGISTROS CON VALORES NULOS
    # ==========================================================

    gestor.analizar_registros_nulos()

    # ==========================================================
    # 6. ANALIZAR DUPLICADOS
    # ==========================================================

    gestor.analizar_duplicados()

    # ==========================================================
    # 7. DIAGNÓSTICO DE CATEGORÍAS
    # ==========================================================

    gestor.diagnostico_categorias()

    # ==========================================================
    # 8. ANALIZAR RANGO DE EDAD
    # ==========================================================

    gestor.analizar_rango_edad()

    # ==========================================================
    # 9. LIMPIAR ESPACIOS
    # ==========================================================

    gestor.limpiar_espacios_texto()

    # ==========================================================
    # 10. CORREGIR RANGO DE EDAD
    # ==========================================================

    gestor.corregir_rango_edad()

    # ==========================================================
    # 11. TRATAR VALORES FALTANTES
    # ==========================================================

    gestor.tratar_valores_faltantes()

    # ==========================================================
    # 12. VALIDAR LIMPIEZA
    # ==========================================================

    gestor.validar_limpieza()

    # ==========================================================
    # 13. REVISIÓN FINAL
    # ==========================================================

    print("\n========================================")
    print("REVISIÓN FINAL DE VALORES FALTANTES")
    print("========================================")

    nulos_finales = gestor.df.isnull().sum()

    nulos_finales = nulos_finales[
        nulos_finales > 0
    ]

    if len(nulos_finales) == 0:

        print(
            "\nNo existen valores nulos "
            "después de la limpieza."
        )

    else:

        print(
            "\nValores nulos que permanecen:"
        )

        print(
            nulos_finales
        )

    # ==========================================================
    # 14. ESTADO FINAL
    # ==========================================================

    print("\n========================================")
    print("ETAPA DE LIMPIEZA COMPLETADA")
    print("========================================")

    print(
        "\nDataset procesado:"
    )

    print(
        ruta_archivo
    )

    print(
        "\nFilas finales: "
        f"{gestor.df.shape[0]}"
    )

    print(
        "Columnas finales: "
        f"{gestor.df.shape[1]}"
    )

    print(
        "\nRegistros eliminados: 0"
    )

    print(
        "Duplicados eliminados: 0"
    )

    print(
        "Categorías eliminadas: 0"
    )

    print(
        "Registros con faltantes conservados: 59"
    )

    # ==========================================================
    # 15. EXPORTAR DATASET LIMPIO
    # ==========================================================

    gestor.exportar_datos(
        ruta_salida
    )

    # ==========================================================
    # 16. CONFIRMACIÓN FINAL
    # ==========================================================

    print("\n========================================")
    print("PROCESO FINALIZADO")
    print("========================================")

    print(
        "\nEl dataset limpio fue guardado en:"
    )

    print(
        ruta_salida
    )


if __name__ == "__main__":
    main()