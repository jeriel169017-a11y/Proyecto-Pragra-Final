import os
from contextlib import asynccontextmanager
import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
MODELO_CLASIFICACION = None
MODELO_REGRESION = None
MODELOS_CARGADOS = False
def buscar_archivo(nombre, carpeta_inicio):
    for root, dirs, files in os.walk(carpeta_inicio):
        if nombre in files:
            return os.path.join(root, nombre)
    return None
@asynccontextmanager
async def lifespan(app: FastAPI):
    global MODELO_CLASIFICACION, MODELO_REGRESION, MODELOS_CARGADOS
    ruta_clf = buscar_archivo("ml_clasificacion_nota.joblib", BASE_DIR)
    ruta_reg = buscar_archivo("ml_regresion_matriculados.joblib", BASE_DIR)
    if ruta_clf and ruta_reg:
        MODELO_CLASIFICACION = joblib.load(ruta_clf)
        MODELO_REGRESION = joblib.load(ruta_reg)
        MODELOS_CARGADOS = True
        print("Modelos cargados correctamente.")
    else:
        MODELOS_CARGADOS = False
        print("AVISO: no se encontraron los .joblib en ninguna subcarpeta de", BASE_DIR)
    yield
app = FastAPI(
    title="API Proyecto - Grupo 6",
    description="Sirven los dos modelos entrenados",
    version="1.0.0",
    lifespan=lifespan)
class DatosAdmision(BaseModel):
    ANO_CONCURSO: int
    SEXO: str
    NACIONALIDAD: str
    RANGO_EDAD: str
    PROVINCIA_RESIDENCIA: str
    CANTON_RESIDENCIA: str
    SEDE: str
    RECINTO: str
    TIPO_COLEGIO: str
    TIPO_HORARIO_COLEGIO: str
    TIPO_MODALIDAD_COLEGIO: str
    PROVINCIA_COLEGIO: str
    CANTON_COLEGIO: str
    TIPO_PROCESO_ADMISION: str
    CARRERA: str
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "ANO_CONCURSO": 2025,
                "SEXO": "Mujer",
                "NACIONALIDAD": "Costarricense",
                "RANGO_EDAD": "17-18",
                "PROVINCIA_RESIDENCIA": "San Jose",
                "CANTON_RESIDENCIA": "Canton A",
                "SEDE": "Sede Central",
                "RECINTO": "Recinto A",
                "TIPO_COLEGIO": "Publico",
                "TIPO_HORARIO_COLEGIO": "Diurno",
                "TIPO_MODALIDAD_COLEGIO": "Academico",
                "PROVINCIA_COLEGIO": "San Jose",
                "CANTON_COLEGIO": "Canton A",
                "TIPO_PROCESO_ADMISION": "Examen de admision",
                "CARRERA": "Ingenieria en Sistemas",
            }
        }
    )
class DatosMatricula(BaseModel):
    AÑO: int
    UNIVERSIDAD: str
    CARRERA: str
    REGION_PLANIFICACION_SEDE: str
    GAM_SEDE: str
    GRADO_ACADEMICO: str
    NIVEL_ACADEMICO: str
    NIVEL_CINE: str
    AREA_CONOCIMIENTO: str
    DISCIPLINA: str
    AREA_UNESCO: str
    DISCIPLINA_UNESCO: str
    STEM_MICITT: str
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "AÑO": 2025,
                "UNIVERSIDAD": "UCR",
                "CARRERA": "Ingenieria en Sistemas",
                "REGION_PLANIFICACION_SEDE": "Central",
                "GAM_SEDE": "Si",
                "GRADO_ACADEMICO": "Bachillerato",
                "NIVEL_ACADEMICO": "Grado",
                "NIVEL_CINE": "6",
                "AREA_CONOCIMIENTO": "Ingenieria",
                "DISCIPLINA": "Ingenieria en Sistemas",
                "AREA_UNESCO": "Ingenieria, Industria y Construccion",
                "DISCIPLINA_UNESCO": "Informatica",
                "STEM_MICITT": "Si",
            }
        }
    )
@app.get("/")
def raiz():
    return {"mensaje": "API Proyecto - Grupo 6", "modelos_cargados": MODELOS_CARGADOS}
@app.get("/health")
def health():
    return {"status": "ok", "modelos_cargados": MODELOS_CARGADOS}
@app.post("/predecir/nota_admision")
def predecir_nota_admision(datos: DatosAdmision):
    if not MODELOS_CARGADOS:
        raise HTTPException(status_code=503, detail="El modelo de clasificacion no esta disponible todavia.")
    try:
        fila = pd.DataFrame([datos.model_dump()])
        prediccion = MODELO_CLASIFICACION.predict(fila)[0]
        return {"rango_nota_admision_predicho": prediccion}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
@app.post("/predecir/matriculados")
def predecir_matriculados(datos: DatosMatricula):
    if not MODELOS_CARGADOS:
        raise HTTPException(status_code=503, detail="El modelo de regresion no esta disponible todavia.")
    try:
        fila = pd.DataFrame([datos.model_dump()])
        prediccion = MODELO_REGRESION.predict(fila)[0]
        return {"matriculados_predicho": round(float(prediccion), 1)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)