# 🎓 Proyecto Final — Análisis, Predicción y Demanda de Educación Superior

## 👥 Grupo #6

**Curso:** BD-143  
**Institución:** Colegio Universitario de Cartago (CUC)

### Integrantes

- 👨‍💻 Jeriel Fonseca
- 👨‍💻 Jefferson Granados
- 👨‍💻 Samiel Jimenez

---

## 📌 Descripción del proyecto

Este proyecto corresponde al trabajo final del curso **BD-143** del **Colegio Universitario de Cartago (CUC)**.

El proyecto desarrolla una solución de análisis de datos y Machine Learning aplicada al ámbito de la **educación superior costarricense**, utilizando información relacionada con admisión universitaria y matrícula.

La solución integra diferentes etapas del proceso de análisis de datos:

- 🧹 Limpieza y preparación de datos
- 🗄️ Gestión y almacenamiento de información
- 📊 Análisis exploratorio de datos (EDA)
- 📈 Visualización de datos
- 🤖 Machine Learning
- 🔌 Desarrollo de una API REST
- 🖥️ Dashboard interactivo
- 🧩 Programación Orientada a Objetos (POO)

El sistema permite analizar información histórica y realizar predicciones sobre:

- 🎯 El rango de nota de admisión.
- 📚 La cantidad de estudiantes matriculados.

---

# 🎯 Objetivo general

Desarrollar una solución de análisis de datos y aprendizaje automático que permita estudiar el comportamiento de la **admisión y matrícula en la educación superior costarricense**, utilizando datos históricos para generar información útil y realizar predicciones sobre el **rango de nota de admisión** y la **cantidad de estudiantes matriculados**.

---

# 🎯 Objetivos específicos

- 🧹 Preparar y limpiar los conjuntos de datos utilizados en el proyecto.
- 📊 Realizar un análisis exploratorio de los datos de admisión y matrícula.
- 📈 Generar visualizaciones para identificar tendencias y patrones.
- 🤖 Implementar modelos de Machine Learning para clasificación y regresión.
- 🎯 Predecir el rango de nota de admisión a partir de características relacionadas con el estudiante y su proceso de admisión.
- 📚 Predecir la cantidad de estudiantes matriculados según características de la universidad, carrera y año.
- 🔌 Exponer los modelos mediante una API desarrollada con FastAPI.
- 🖥️ Crear un dashboard interactivo mediante Streamlit.
- 🧩 Aplicar Programación Orientada a Objetos en los componentes correspondientes.
- 📦 Mantener una estructura modular y organizada del proyecto.

---
# 🗃️ Fuentes de datos

El proyecto utiliza información relacionada con la educación superior costarricense.

Los datos originales se encuentran en:

```text
data/raw/
y los procesados

data/processed/
conare_admision_limpio.csv
conare_matricula_limpio.csv
matricula_agregada_modelo.csv

Análisis exploratorio de datos

El proyecto incluye un proceso de análisis exploratorio de datos (EDA) para identificar características, tendencias y relaciones presentes en los conjuntos de datos.

Los resultados se encuentran en:

data/resultados/

Los indicadores académicos se almacenan en:

data/resultados/analisis_academico/indicadores_academicos.csv
📈 Visualizaciones

Se generaron diferentes gráficos para analizar los datos de matrícula y admisión.

Las visualizaciones se encuentran en:

data/resultados/graficos/

Entre los análisis realizados se incluyen:

Matrícula por año.
Matrícula por universidad.
Tipo de matrícula.
Matrícula por sexo.
STEM vs. no STEM.
Distribución de edad.
Matrícula por provincia.
Área de conocimiento.
Admisión por año.
Rango de edad de admisión.
Rango de nota de admisión.
Tipo de colegio.
Modalidad del colegio.
Horario del colegio.
Proceso de admisión.
Admisión por sexo.
Admisión por provincia.
Sexo vs. tipo de matrícula.
STEM vs. sexo.
Universidad vs. tipo de matrícula.


### BLOQUE 3 — Machine Learning


```markdown
# 🤖 Machine Learning


El proyecto implementa dos modelos de aprendizaje automático:


1. 🎯 Clasificación del rango de nota de admisión.
2. 📚 Regresión de la cantidad de estudiantes matriculados.


---


## 🎯 Modelo de clasificación — Rango de nota de admisión


Para la predicción del rango de nota de admisión se utiliza un modelo de:


**Regresión Logística (Logistic Regression)**


Las variables utilizadas incluyen:


- `ANO_CONCURSO`
- `SEXO`
- `NACIONALIDAD`
- `RANGO_EDAD`
- `PROVINCIA_RESIDENCIA`
- `CANTON_RESIDENCIA`
- `SEDE`
- `RECINTO`
- `TIPO_COLEGIO`
- `TIPO_HORARIO_COLEGIO`
- `TIPO_MODALIDAD_COLEGIO`
- `PROVINCIA_COLEGIO`
- `CANTON_COLEGIO`
- `TIPO_PROCESO_ADMISION`
- `CARRERA`


Para el procesamiento de las variables se utilizan técnicas como:


- `SimpleImputer`
- `OneHotEncoder`
- `ColumnTransformer`
- `Pipeline`


El modelo entrenado se guarda como:


```text
src/modelos/ml_clasificacion_nota.joblib
📚 Modelo de regresión — Cantidad de matriculados

Para estimar la cantidad de estudiantes matriculados se utiliza:

Decision Tree Regressor

La información se agrupa principalmente por:

Año.
Universidad.
Carrera.

Además, se utilizan características como:

REGION_PLANIFICACION_SEDE
GAM_SEDE
GRADO_ACADEMICO
NIVEL_ACADEMICO
NIVEL_CINE
AREA_CONOCIMIENTO
DISCIPLINA
AREA_UNESCO
DISCIPLINA_UNESCO
STEM_MICITT

El modelo entrenado se guarda como:

src/modelos/ml_regresion_matriculados.joblib

También se genera:

data/processed/matricula_agregada_modelo.csv
📈 Resultados de los modelos
🎯 Clasificación
Métrica	Resultado
Accuracy	0.7137
Precision weighted	0.7105
Recall weighted	0.7137
F1 weighted	0.7011
📚 Regresión
Métrica	Resultado
MAE	25.61
RMSE	81.91
R²	0.9703

Estos resultados corresponden a la evaluación realizada durante el entrenamiento de los modelos.



### BLOQUE 4 — API


```markdown
# 🔌 API REST


El proyecto cuenta con una API REST desarrollada utilizando **FastAPI**.


La API permite cargar los modelos entrenados y utilizarlos para realizar predicciones.


---


## ❤️ Estado de la API


Endpoint:


```http
GET /health

Este endpoint permite comprobar si la API está funcionando y si los modelos fueron cargados correctamente.

Ejemplo:

{
  "status": "ok",
  "modelos_cargados": true
}
🎯 Predicción del rango de nota de admisión

Endpoint:

POST /predecir/nota_admision

Recibe las características correspondientes a una persona y devuelve el rango de nota de admisión predicho.

Ejemplo de respuesta:

{
  "rango_nota_admision_predicho": "..."
}
📚 Predicción de matriculados

Endpoint:

POST /predecir/matriculados

Recibe las características correspondientes a la universidad, carrera, año y demás variables utilizadas por el modelo.

Ejemplo de respuesta:

{
  "matriculados_predicho": 123.4
}
📖 Documentación de la API

FastAPI proporciona documentación interactiva mediante Swagger.

Una vez iniciada la API:

http://127.0.0.1:8000/docs

También se puede consultar:

http://127.0.0.1:8000/health


### BLOQUE 5 — Dashboard


```markdown
# 🖥️ Dashboard interactivo


El proyecto incluye un dashboard desarrollado con **Streamlit**.


El dashboard permite utilizar los modelos de Machine Learning mediante una interfaz gráfica.


---


## 🎯 Rango de nota de admisión


La primera sección permite ingresar información relacionada con:


- Año de concurso.
- Sexo.
- Nacionalidad.
- Rango de edad.
- Provincia de residencia.
- Cantón de residencia.
- Sede.
- Recinto.
- Tipo de colegio.
- Horario del colegio.
- Modalidad del colegio.
- Provincia del colegio.
- Cantón del colegio.
- Proceso de admisión.
- Carrera.


Al enviar la información, el dashboard consulta la API y muestra el **rango de nota de admisión predicho**.


---


## 📈 Demanda de matrícula


La segunda sección permite ingresar información relacionada con:


- Año.
- Universidad.
- Carrera.
- Región de planificación.
- Ubicación GAM.
- Grado académico.
- Nivel académico.
- Nivel CINE.
- Área de conocimiento.
- Disciplina.
- Área UNESCO.
- Disciplina UNESCO.
- Clasificación STEM MICITT.


Al enviar la información, el dashboard consulta la API y muestra la **cantidad de matriculados predicha**.


---
# 🧩 Programación Orientada a Objetos

El proyecto incorpora **Programación Orientada a Objetos (POO)** en los componentes correspondientes.

La organización modular permite separar responsabilidades relacionadas con:

- 🗄️ Gestión de base de datos.
- 📂 Gestión de datos.
- 📊 Análisis.
- 🧹 Procesamiento EDA.
- 📈 Visualización.
- 🛠️ Funciones auxiliares.

Esta organización facilita el mantenimiento, reutilización y separación de responsabilidades dentro del proyecto.

---

# ⚙️ Tecnologías utilizadas

| Tecnología | Uso |
|---|---|
| 🐍 Python | Lenguaje principal |
| 🐼 Pandas | Manipulación y análisis de datos |
| 🔢 NumPy | Operaciones numéricas |
| 📊 Matplotlib | Visualización |
| 🤖 Scikit-learn | Machine Learning |
| 📦 Joblib | Persistencia de modelos |
| 🚀 FastAPI | Desarrollo de API REST |
| 🦄 Uvicorn | Servidor de la API |
| 🖥️ Streamlit | Dashboard interactivo |
| 🗄️ SQL Server | Gestión de base de datos |
| 📄 CSV / Excel | Fuentes de datos |

---

# 📁 Estructura del proyecto

```text
Proyecto-Pragra-Final/
│
├── 📄 .gitattributes
├── 📄 .gitignore
├── 📄 README.md
├── 📄 requirements.txt
├── 📄 main.py
│
├── 📁 dashboard/
│   └── 📄 app.py
│
├── 📁 data/
│   │
│   ├── 📁 raw/
│   │   ├── bd_matricula_sector_estatal_2021_2025.xlsx
│   │   └── datos_poblacion_admitida_de_primer_ingreso_pregrado_y_grado_ucr_csv.csv
│   │
│   ├── 📁 processed/
│   │   ├── conare_admision_limpio.csv
│   │   ├── conare_matricula_limpio.csv
│   │   └── matricula_agregada_modelo.csv
│   │
│   └── 📁 resultados/
│       │
│       ├── 📁 analisis_academico/
│       │   └── indicadores_academicos.csv
│       │
│       └── 📁 graficos/
│           ├── 01_matricula_por_anio.png
│           ├── 02_matricula_por_universidad.png
│           ├── 03_tipo_matricula.png
│           ├── 04_matricula_por_sexo.png
│           ├── 05_stem_vs_no_stem.png
│           ├── 06_distribucion_edad.png
│           ├── 07_matricula_por_provincia.png
│           ├── 08_area_conocimiento.png
│           ├── 09_admision_por_anio.png
│           ├── 10_rango_edad_admision.png
│           ├── 11_rango_nota_admision.png
│           ├── 12_tipo_colegio.png
│           ├── 13_modalidad_colegio.png
│           ├── 14_horario_colegio.png
│           ├── 15_proceso_admision.png
│           ├── 16_admision_por_sexo.png
│           ├── 17_admision_por_provincia.png
│           ├── 18_sexo_vs_tipo_matricula.png
│           ├── 19_stem_vs_sexo.png
│           └── 20_universidad_vs_tipo_matricula.png
│
├── 📁 database/
│   └── DesercionEstudiantil.bak
│
└── 📁 src/
    │
    ├── 📄 __init__.py
    ├── 📄 cargar_datos_sql.py
    ├── 📄 comprobar_datasets.py
    │
    ├── 📁 analisis/
    │   └── 📄 analizador_academico.py
    │
    ├── 📁 api/
    │   ├── 📄 __init__.py
    │   └── 📄 cliente_api.py
    │
    ├── 📁 basedatos/
    │   ├── 📄 __init__.py
    │   └── 📄 gestor_base_datos.py
    │
    ├── 📁 datos/
    │   ├── 📄 __init__.py
    │   └── 📄 gestor_datos.py
    │
    ├── 📁 eda/
    │   ├── 📄 __init__.py
    │   └── 📄 procesador_eda.py
    │
    ├── 📁 helpers/
    │   ├── 📄 __init__.py
    │   └── 📄 utilidades.py
    │
    ├── 📁 modelos/
    │   ├── 📄 __init__.py
    │   ├── 📄 modelo_ml.py
    │   ├── 📦 ml_clasificacion_nota.joblib
    │   └── 📦 ml_regresion_matriculados.joblib
    │
    └── 📁 visualizacion/
        ├── 📄 __init__.py
        └── 📄 visualizador.py

### BLOQUE 7 — Instalación, ejecución y cierre

```markdown
# 🚀 Instalación y ejecución

## 1️⃣ Clonar el repositorio

```bash
git clone <URL_DEL_REPOSITORIO>
cd Proyecto-Pragra-Final

Crear el entorno virtual

En Windows:

python -m venv .venv

Activar el entorno:

.venv\Scripts\activate
3️⃣ Instalar las dependencias
pip install -r requirements.txt
🤖 Entrenar los modelos

Para entrenar nuevamente los modelos:

python src/modelos/modelo_ml.py

Al finalizar correctamente se generan:

src/modelos/ml_clasificacion_nota.joblib
src/modelos/ml_regresion_matriculados.joblib
🔌 Ejecutar la API

Desde la carpeta raíz del proyecto:

uvicorn src.api.cliente_api:app --reload

La API estará disponible en:

http://127.0.0.1:8000

Documentación:

http://127.0.0.1:8000/docs

Estado:

http://127.0.0.1:8000/health

Ejecutar el dashboard

Con la API ejecutándose, abrir otra terminal y ejecutar:

streamlit run dashboard/app.py
🔄 Flujo general
📥 Datos originales
       │
       ▼
🧹 Limpieza y preparación
       │
       ▼
📂 Datos procesados
       │
       ├──────────────► 📊 EDA
       │                    │
       │                    ▼
       │                📈 Visualizaciones
       │
       ▼
🤖 Machine Learning
       │
       ├──────────────► 🎯 Clasificación
       │
       └──────────────► 📚 Regresión
                            │
                            ▼
                     📦 Modelos .joblib
                            │
                            ▼
                       🔌 FastAPI
                            │
                            ▼
                       🖥️ Streamlit
                            │
                            ▼
                     👤 Usuario final
🔁 Funcionamiento de las predicciones

El funcionamiento general del sistema es:

👤 El usuario introduce los datos en el dashboard.
🖥️ Streamlit prepara la solicitud.
🔌 La solicitud se envía a FastAPI.
🚀 FastAPI valida los datos recibidos.
🤖 Se utiliza el modelo correspondiente.
📊 El modelo genera la predicción.
🔙 FastAPI devuelve el resultado.
🖥️ Streamlit muestra la predicción al usuario.
📌 Consideraciones
La API debe estar ejecutándose para utilizar el dashboard.
Los modelos .joblib deben estar disponibles para que la API pueda cargarlos.
Los datos procesados utilizados durante el entrenamiento se encuentran en data/processed/.
Los valores introducidos en el dashboard deben ser compatibles con las variables utilizadas por los modelos.
