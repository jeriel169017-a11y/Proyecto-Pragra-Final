import pyodbc
import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote_plus
# Clase encargada de gestionar la conexion y las consultas a SQL Sever
# Utiliza autenticacion de  Windows
class GestorBaseDatos:
    def __init__(
        self,
        servidor,
        base_datos,
        driver="ODBC Driver 17 for SQL Server"):
        self.servidor = servidor
        self.base_datos = base_datos
        self.driver = driver
        self.conexion = None
        self.engine = None
    # Conexion
    # Establece la conexion con SQL Server
    def conectar(self):
        print("\n========================================")
        print("CONEXIÓN A SQL SERVER")
        print("========================================")
        cadena_conexion = (
            f"DRIVER={{{self.driver}}};"
            f"SERVER={self.servidor};"
            f"DATABASE={self.base_datos};"
            "Trusted_Connection=yes;"
        )
        try:
            # Conexión pyodbc
            self.conexion = pyodbc.connect(
                cadena_conexion)
            # Crear engine de SQLAlchemy
            parametros = quote_plus(
                cadena_conexion)
            cadena_engine = (
                "mssql+pyodbc:///?odbc_connect="
                + parametros)
            self.engine = create_engine(
                cadena_engine)
            print("\nConexión establecida correctamente.")
            print(f"Servidor: {self.servidor}")
            print(f"Base de datos: {self.base_datos}")
        except Exception as error:
            print("\nERROR AL CONECTAR CON SQL SERVER.")
            print(error)
            raise
    # Ejecutar consulta
    # Ejecuta una consulta SQL y devuelve los resultados como DataFrame
    def ejecutar_consulta(self, consulta):
        if self.engine is None:
            raise ConnectionError(
                "No existe una conexión activa "
                "con SQL Server.")
        try:
            df = pd.read_sql(
                consulta,
                self.engine)
            print("\nConsulta ejecutada correctamente.")
            print(f"Registros obtenidos: {len(df)}")
            return df
        except Exception as error:
            print("\nERROR AL EJECUTAR LA CONSULTA.")
            print(error)
            raise
    # Cerrar conexion
    # Cierra la conexion activa con SQL Server
    def cerrar_conexion(self):
        # Cerrar engine
        if self.engine is not None:
            self.engine.dispose()
            self.engine = None
        # Cerrar conexión pyodbc
        if self.conexion is not None:
            self.conexion.close()
            self.conexion = None
        print("\nConexión cerrada correctamente.")