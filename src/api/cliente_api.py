import os
from contextlib import asynccontextmanager
import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
MODELS = os.path.join(BASE_DIR, "models")
MODELO_CLASIFICACION = None
MODELO_REGRESION = None
MODELOS_CARGADOS = False
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Se ejecuta al arrancar la API (reemplaza al @app.on_event("startup") deprecado)
    global MODELO_CLASIFICACION, MODELO_REGRESION, MODELOS_CARGADOS
    ruta_clf = os.path.join(MODELS, "modelo_clasificacion_nota.joblib")
    ruta_reg = os.path.join(MODELS, "modelo_regresion_matriculados.joblib")
    if os.path.exists(ruta_clf) and os.path.exists(ruta_reg):
        MODELO_CLASIFICACION = joblib.load(ruta_clf)
        MODELO_REGRESION = joblib.load(ruta_reg)
        MODELOS_CARGADOS = True
        print("Modelos cargados correctamente.")
    else:
        MODELOS_CARGADOS = False
        print("AVISO: no se encontraron los .joblib en 'models/'.""Ejecute primero src/modelos/modelos.py para generarlos.")
    yield
app = FastAPI(
    title="API Proyecto - Grupo 6",
    description="Sirven los dos modelos entrenados",
    version="1.0.0",
    lifespan=lifespan)
# ESQUEMAS DE ENTRADA (mismas columnas que "features" y "features_r" en modelos.py, sin agregar ni quitar ninguna)
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
                "PROVINCIA_RESIDENCIA": "San José",
                "CANTON_RESIDENCIA": "Cantón A",
                "SEDE": "Sede Central",
                "RECINTO": "Recinto A",
                "TIPO_COLEGIO": "Público",
                "TIPO_HORARIO_COLEGIO": "Diurno",
                "TIPO_MODALIDAD_COLEGIO": "Académico",
                "PROVINCIA_COLEGIO": "San José",
                "CANTON_COLEGIO": "Cantón A",
                "TIPO_PROCESO_ADMISION": "Examen de admisión",
                "CARRERA": "Ingeniería en Sistemas",
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
                "CARRERA": "Ingeniería en Sistemas",
                "REGION_PLANIFICACION_SEDE": "Central",
                "GAM_SEDE": "Sí",
                "GRADO_ACADEMICO": "Bachillerato",
                "NIVEL_ACADEMICO": "Grado",
                "NIVEL_CINE": "6",
                "AREA_CONOCIMIENTO": "Ingeniería",
                "DISCIPLINA": "Ingeniería en Sistemas",
                "AREA_UNESCO": "Ingeniería, Industria y Construcción",
                "DISCIPLINA_UNESCO": "Informática",
                "STEM_MICITT": "Sí",
            }
        }
    )
# ENDPOINTS
@app.get("/")
def raiz():
    return {"mensaje": "API Proyecto - Grupo 6", "modelos_cargados": MODELOS_CARGADOS}
@app.get("/health")
def health():
    return {"status": "ok", "modelos_cargados": MODELOS_CARGADOS}
@app.post("/predecir/nota_admision")
def predecir_nota_admision(datos: DatosAdmision):
    if not MODELOS_CARGADOS:
        raise HTTPException(status_code=503, detail="El modelo de clasificación no está disponible todavía.")
    try:
        fila = pd.DataFrame([datos.model_dump()])
        prediccion = MODELO_CLASIFICACION.predict(fila)[0]
        return {"rango_nota_admision_predicho": prediccion}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
@app.post("/predecir/matriculados")
def predecir_matriculados(datos: DatosMatricula):
    if not MODELOS_CARGADOS:
        raise HTTPException(status_code=503, detail="El modelo de regresión no está disponible todavía.")
    try:
        fila = pd.DataFrame([datos.model_dump()])
        prediccion = MODELO_REGRESION.predict(fila)[0]
        return {"matriculados_predicho": round(float(prediccion), 1)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
# Arranque directo (para poder correr este archivo con el botón de PyCharm, sin necesitar el comando "uvicorn" a mano)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)