from fastapi import FastAPI
from fastapi.responses import JSONResponse
import os
import joblib
import pandas as pd
app = FastAPI(
    title="API de Predicciones",
    description="API para predicción de nota de admisión y cantidad de matriculados"
)
# Cargar modelos
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
modelo_clasificacion = joblib.load(
    os.path.join(BASE_DIR, "modelos", "ml_clasificacion_nota.joblib")
)
modelo_regresion = joblib.load(
    os.path.join(BASE_DIR, "modelos", "ml_regresion_matriculados.joblib")
)
@app.get("/")
def inicio():
    return JSONResponse(
        content={
            "mensaje": "API funcionando correctamente"
        }
    )
@app.get("/health")
def health():
    return JSONResponse(
        content={
            "estado": "API funcionando",
            "modelos_cargados": True
        }
    )
@app.post("/predecir/nota_admision")
def predecir_nota_admision(datos: dict):
    try:
        df = pd.DataFrame([datos])
        prediccion = modelo_clasificacion.predict(df)[0]
        return JSONResponse(
            content={
                "rango_nota_admision_predicho": str(prediccion)
            }
        )
    except Exception as e:
        return JSONResponse(
            content={
                "error": f"Error al predecir la nota de admisión: {str(e)}"
            },
            status_code=500
        )
@app.post("/predecir/matriculados")
def predecir_matriculados(datos: dict):
    try:
        df = pd.DataFrame([datos])
        prediccion = modelo_regresion.predict(df)[0]
        return JSONResponse(
            content={
                "matriculados_predicho": float(prediccion)
            }
        )
    except Exception as e:
        return JSONResponse(
            content={
                "error": f"Error al predecir los matriculados: {str(e)}"
            },
            status_code=500
        )
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000
    )