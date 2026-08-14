import os
import pandas as pd


class GestorDatos:
    """
    Clase encargada de cargar, analizar, limpiar,
    transformar, validar y exportar el segundo dataset.
    """

    def __init__(self, ruta_archivo):
        self.ruta_archivo = ruta_archivo
        self.df = None

    # ==========================================================
    # CARGAR DATOS
    # ==========================================================

    def cargar_datos(self):
        print("\n========================================")
        print("CARGANDO DATOS")
        print("========================================")

        extension = os.path.splitext(self.ruta_archivo)[1].lower()

        if extension == ".xlsx":

            self.df = pd.read_excel(self.ruta_archivo)

        elif extension == ".csv":

            configuraciones = [
                {"encoding": "utf-8-sig", "sep": ","},
                {"encoding": "utf-8", "sep": ","},
                {"encoding": "cp1252", "sep": ","},
                {"encoding": "latin1", "sep": ","},
                {"encoding": "utf-8-sig", "sep": ";"},
                {"encoding": "utf-8", "sep": ";"},
                {"encoding": "cp1252", "sep": ";"},
                {"encoding": "latin1", "sep": ";"}
            ]

            cargado = False

            for configuracion in configuraciones:

                try:

                    df_prueba = pd.read_csv(
                        self.ruta_archivo,
                        encoding=configuracion["encoding"],
                        sep=configuracion["sep"]
                    )

                    if len(df_prueba.columns) > 1:
                        self.df = df_prueba
                        cargado = True
                        break

                except Exception:
                    continue

            if not cargado:
                raise ValueError(
                    "No fue posible leer el archivo CSV."
                )

        else:

            raise ValueError(
                "Formato no compatible. "
                "Utilice un archivo .xlsx o .csv."
            )

        print("\nArchivo cargado correctamente.")

        print(
            f"Filas: {self.df.shape[0]}"
        )

        print(
            f"Columnas: {self.df.shape[1]}"
        )

        return self.df

    # ==========================================================
    # CORRECCIÓN DE ENCABEZADOS
    # ==========================================================

    def corregir_encabezados(self):
        print("\n========================================")
        print("CORRECCIÓN DE ENCABEZADOS")
        print("========================================")

        encabezados_ajustados = 0
        columnas_nuevas = []

        for columna in self.df.columns:

            columna_original = columna

            columna_nueva = str(columna).strip()

            columna_nueva = columna_nueva.replace(
                "ï»¿",
                ""
            )

            if columna_original != columna_nueva:

                print(
                    f"{columna_original} -> "
                    f"{columna_nueva}"
                )

                encabezados_ajustados += 1

            columnas_nuevas.append(columna_nueva)

        self.df.columns = columnas_nuevas

        print(
            f"\nEncabezados ajustados: "
            f"{encabezados_ajustados}"
        )

    # ==========================================================
    # INFORMACIÓN GENERAL
    # ==========================================================

    def mostrar_informacion_general(self):

        print("\n========================================")
        print("INFORMACIÓN GENERAL")
        print("========================================")

        print(
            f"Filas: {self.df.shape[0]}"
        )

        print(
            f"Columnas: {self.df.shape[1]}"
        )

        print("\nColumnas:")

        print(
            list(self.df.columns)
        )

        print("\nTipos de datos:")

        print(
            self.df.dtypes
        )

    # ==========================================================
    # VALORES NULOS
    # ==========================================================

    def analizar_nulos(self):

        print("\n========================================")
        print("ANÁLISIS DE VALORES NULOS")
        print("========================================")

        nulos = self.df.isnull().sum()

        nulos = nulos[nulos > 0]

        if len(nulos) == 0:

            print(
                "No se encontraron valores nulos."
            )

        else:

            print(nulos)

    # ==========================================================
    # REGISTROS CON VALORES NULOS
    # ==========================================================

    def analizar_registros_nulos(self):

        print("\n========================================")
        print("ANÁLISIS DE REGISTROS CON VALORES NULOS")
        print("========================================")

        mascara_nulos = self.df.isnull().any(axis=1)

        registros_nulos = self.df[mascara_nulos]

        cantidad = len(registros_nulos)

        print(
            "\nCantidad de registros con al menos "
            f"un valor nulo: {cantidad}"
        )

        if cantidad == 0:

            print(
                "\nNo se encontraron registros "
                "con valores nulos."
            )

            return

        print(
            "\nColumnas que presentan valores "
            "nulos en estos registros:"
        )

        columnas_nulas = registros_nulos.isnull().sum()

        columnas_nulas = columnas_nulas[
            columnas_nulas > 0
        ]

        print(columnas_nulas)

        print(
            "\nDetalle de los registros:"
        )

        print(
            registros_nulos.to_string(
                index=False
            )
        )

        print(
            "\n========================================"
        )

        print(
            "Este análisis NO modifica los datos."
        )

        print(
            "Los registros con valores nulos "
            "NO fueron eliminados."
        )

        print(
            "========================================"
        )

    # ==========================================================
    # DUPLICADOS
    # ==========================================================

    def analizar_duplicados(self):

        print("\n========================================")
        print("ANÁLISIS DE DUPLICADOS")
        print("========================================")

        total_duplicados = self.df.duplicated().sum()

        print(
            "Registros duplicados exactos: "
            f"{total_duplicados}"
        )

        if total_duplicados == 0:

            print(
                "No se encontraron duplicados."
            )

        else:

            print(
                "Los duplicados se conservan "
                "por ahora."
            )

    # ==========================================================
    # DIAGNÓSTICO DE CATEGORÍAS
    # ==========================================================

    def diagnostico_categorias(self):

        print("\n========================================")
        print("DIAGNÓSTICO DE CATEGORÍAS")
        print("========================================")

        columnas = [
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

        for columna in columnas:

            if columna not in self.df.columns:
                continue

            print(
                "\n----------------------------------------"
            )

            print(
                f"COLUMNA: {columna}"
            )

            print(
                "----------------------------------------"
            )

            print(
                "Valores únicos: "
                f"{self.df[columna].nunique(dropna=True)}"
            )

            print(
                "\nValores más frecuentes:"
            )

            print(
                self.df[columna]
                .value_counts(dropna=False)
                .head(15)
            )

    # ==========================================================
    # ANÁLISIS DE RANGO DE EDAD
    # ==========================================================

    def analizar_rango_edad(self):

        print("\n========================================")
        print("ANÁLISIS DE RANGO DE EDAD")
        print("========================================")

        if "RANGO_EDAD" not in self.df.columns:

            print(
                "La columna RANGO_EDAD no existe."
            )

            return

        print(
            "\nTipo de dato:"
        )

        print(
            self.df["RANGO_EDAD"].dtype
        )

        print(
            "\nValores únicos:"
        )

        print(
            self.df["RANGO_EDAD"].nunique(
                dropna=True
            )
        )

        print(
            "\nFrecuencia de valores:"
        )

        print(
            self.df["RANGO_EDAD"]
            .value_counts(dropna=False)
        )

    # ==========================================================
    # LIMPIEZA DE ESPACIOS EN TEXTO
    # ==========================================================

    def limpiar_espacios_texto(self):

        print("\n========================================")
        print("LIMPIEZA DE ESPACIOS EN TEXTO")
        print("========================================")

        total_ajustados = 0

        columnas_texto = self.df.select_dtypes(
            include=["object", "string"]
        ).columns

        for columna in columnas_texto:

            antes = self.df[columna].copy()

            self.df[columna] = (
                self.df[columna]
                .astype("string")
                .str.replace(
                    "\r",
                    " ",
                    regex=False
                )
                .str.replace(
                    "\n",
                    " ",
                    regex=False
                )
                .str.replace(
                    "\t",
                    " ",
                    regex=False
                )
                .str.strip()
            )

            ajustados = (
                antes.astype("string")
                != self.df[columna]
            ).sum()

            if ajustados > 0:

                print(
                    f"{columna}: "
                    f"{ajustados} valores ajustados"
                )

                total_ajustados += ajustados

        print(
            "\nTotal de valores ajustados: "
            f"{total_ajustados}"
        )

    # ==========================================================
    # CORRECCIÓN DE RANGO DE EDAD
    # ==========================================================

    def corregir_rango_edad(self):

        print("\n========================================")
        print("CORRECCIÓN DE RANGO DE EDAD")
        print("========================================")

        if "RANGO_EDAD" not in self.df.columns:

            print(
                "La columna RANGO_EDAD no existe."
            )

            return

        print(
            "\nValores antes de la corrección:"
        )

        print(
            self.df["RANGO_EDAD"]
            .value_counts(dropna=False)
        )

        self.df["RANGO_EDAD"] = (
            self.df["RANGO_EDAD"]
            .replace(
                {
                    "25 o mÃ¡s": "25 o más",
                    "25 o mÃ¡s ": "25 o más"
                }
            )
        )

        print(
            "\nValores después de la corrección:"
        )

        print(
            self.df["RANGO_EDAD"]
            .value_counts(dropna=False)
        )

        print(
            "\nCorrección de RANGO_EDAD "
            "completada."
        )

        print(
            "No se eliminaron registros."
        )

        print(
            "No se eliminaron categorías."
        )

    # ==========================================================
    # TRATAMIENTO DE VALORES FALTANTES
    # ==========================================================

    def tratar_valores_faltantes(self):

        print("\n========================================")
        print("TRATAMIENTO DE VALORES FALTANTES")
        print("========================================")

        nulos_antes = self.df.isnull().sum()

        nulos_antes = nulos_antes[
            nulos_antes > 0
        ]

        if len(nulos_antes) == 0:

            print(
                "\nNo existen valores faltantes."
            )

            return

        print(
            "\nValores faltantes encontrados:"
        )

        print(nulos_antes)

        print(
            "\nDECISIÓN:"
        )

        print(
            "Los registros con valores faltantes "
            "NO serán eliminados."
        )

        print(
            "Los valores faltantes de "
            "PROVINCIA_COLEGIO y CANTON_COLEGIO "
            "se conservarán como NaN."
        )

        print(
            "\nJustificación:"
        )

        print(
            "Los 59 registros contienen información "
            "válida en el resto de sus variables."
        )

        print(
            "Eliminar estos registros provocaría "
            "pérdida innecesaria de información."
        )

        print(
            "\nTratamiento completado."
        )

    # ==========================================================
    # VALIDACIÓN DE LIMPIEZA
    # ==========================================================

    def validar_limpieza(self):

        print("\n========================================")
        print("VALIDACIÓN DE LIMPIEZA")
        print("========================================")

        print(
            "\nDimensiones actuales:"
        )

        print(
            f"Filas: {self.df.shape[0]}"
        )

        print(
            f"Columnas: {self.df.shape[1]}"
        )

        print(
            "\nValores nulos por columna:"
        )

        nulos = self.df.isnull().sum()

        nulos = nulos[nulos > 0]

        if len(nulos) == 0:

            print(
                "No hay valores nulos."
            )

        else:

            print(nulos)

        if "RANGO_EDAD" in self.df.columns:

            print(
                "\nValidación específica de "
                "RANGO_EDAD:"
            )

            print(
                "Tipo: "
                f"{self.df['RANGO_EDAD'].dtype}"
            )

            print(
                "Valores únicos: "
                f"{self.df['RANGO_EDAD'].nunique(dropna=True)}"
            )

            print(
                "\nCategorías:"
            )

            print(
                self.df["RANGO_EDAD"]
                .value_counts(dropna=False)
            )

    # ==========================================================
    # EXPORTAR
    # ==========================================================

    def exportar_datos(self, ruta_salida):

        print("\n========================================")
        print("EXPORTACIÓN DE DATOS")
        print("========================================")

        carpeta = os.path.dirname(ruta_salida)

        if carpeta:

            os.makedirs(
                carpeta,
                exist_ok=True
            )

        self.df.to_csv(
            ruta_salida,
            index=False,
            encoding="utf-8-sig"
        )

        print(
            "\nArchivo exportado correctamente:"
        )

        print(
            ruta_salida
        )

        print(
            f"\nFilas exportadas: "
            f"{self.df.shape[0]}"
        )

        print(
            f"Columnas exportadas: "
            f"{self.df.shape[1]}"
        )