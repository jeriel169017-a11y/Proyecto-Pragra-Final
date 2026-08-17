
import os
import requests
import streamlit as st
API_URL = os.environ.get("API_URL", "http://127.0.0.1:8000")
st.set_page_config(page_title="Proyecto Grupo 6", layout="wide")
st.title("Predicción de Nota de Admisión y Demanda de Matrícula")
st.caption("Colegio Universitario de Cartago · BD-143 · Grupo #6")
def revisar_api():
    try:
        r = requests.get(f"{API_URL}/health", timeout=5)
        r.raise_for_status()
        return r.json()
    except requests.RequestException:
        return None
estado = revisar_api()
with st.sidebar:
    st.header("Estado de la API")
    st.code(API_URL)
    if estado is None:
        st.error("No se pudo conectar a la API. ¿Está corriendo `uvicorn src.api.main:app`?")
    elif not estado.get("modelos_cargados"):
        st.warning("La API responde, pero los modelos aún no están entrenados/cargados.")
    else:
        st.success("API conectada y modelos listos ✅")
tab_admision, tab_matricula = st.tabs(["🎯 Rango de nota de admisión", "📈 Demanda de matrícula"])
# TAB 1: Clasificación - Rango_Nota_Admision
with tab_admision:
    st.subheader("Predecir rango de nota de admisión")
    with st.form("form_admision"):
        col1, col2, col3 = st.columns(3)
        with col1:
            ano_concurso = st.number_input("Año de concurso", min_value=2000, max_value=2100, value=2025)
            sexo = st.text_input("Sexo", value="Mujer")
            nacionalidad = st.text_input("Nacionalidad", value="Costarricense")
            rango_edad = st.text_input("Rango de edad", value="18 o menos")
            provincia_residencia = st.text_input("Provincia de residencia", value="San José")
        with col2:
            canton_residencia = st.text_input("Cantón de residencia", value="San José")
            sede = st.text_input("Sede", value="10 - SEDE RODRIGO FACIO")
            recinto = st.text_input("Recinto", value="11 - CIUDAD UNIVERSITARIA RODRIGO FACIO")
            tipo_colegio = st.text_input("Tipo de colegio", value="PUBLICO")
            tipo_horario_colegio = st.text_input("Tipo de horario del colegio", value="DIURNO")
        with col3:
            tipo_modalidad_colegio = st.text_input("Tipo de modalidad del colegio", value="ACADEMICO")
            provincia_colegio = st.text_input("Provincia del colegio", value="San José")
            canton_colegio = st.text_input("Cantón del colegio", value="San José")
            tipo_proceso_admision = st.text_input("Tipo de proceso de admisión", value="ORDINARIA")
            carrera = st.text_input(
                "Carrera",
                value="420703 - BACHILLERATO Y LICENCIATURA EN COMPUTACIÓN E INFORMÁTICA",)
        enviar_admision = st.form_submit_button("Predecir rango de nota")
    if enviar_admision:
        payload = {
            "ANO_CONCURSO": ano_concurso,
            "SEXO": sexo,
            "NACIONALIDAD": nacionalidad,
            "RANGO_EDAD": rango_edad,
            "PROVINCIA_RESIDENCIA": provincia_residencia,
            "CANTON_RESIDENCIA": canton_residencia,
            "SEDE": sede,
            "RECINTO": recinto,
            "TIPO_COLEGIO": tipo_colegio,
            "TIPO_HORARIO_COLEGIO": tipo_horario_colegio,
            "TIPO_MODALIDAD_COLEGIO": tipo_modalidad_colegio,
            "PROVINCIA_COLEGIO": provincia_colegio,
            "CANTON_COLEGIO": canton_colegio,
            "TIPO_PROCESO_ADMISION": tipo_proceso_admision,
            "CARRERA": carrera}
        try:
            r = requests.post(f"{API_URL}/predecir/nota_admision", json=payload, timeout=10)
            r.raise_for_status()
            resultado = r.json()
            st.success(f"Rango de nota de admisión predicho: **{resultado['rango_nota_admision_predicho']}**")
        except requests.RequestException as e:
            st.error(f"Error al consultar la API: {e}")
# TAB 2: Regresión - Matriculados
with tab_matricula:
    st.subheader("Predecir cantidad de matriculados")
    with st.form("form_matricula"):
        col1, col2, col3 = st.columns(3)
        with col1:
            anio = st.number_input("Año", min_value=2000, max_value=2100, value=2025)
            universidad = st.text_input("Universidad", value="Universidad de Costa Rica")
            carrera_m = st.text_input("Carrera", value="Computación e Informática")
            region_planificacion_sede = st.text_input("Región de planificación de la sede", value="Región Central")
            gam_sede = st.text_input("¿Sede en GAM?", value="GAM")
        with col2:
            grado_academico = st.text_input("Grado académico", value="Bachillerato")
            nivel_academico = st.text_input("Nivel académico", value="Grado")
            nivel_cine = st.text_input("Nivel CINE", value="CINE 6")
            area_conocimiento = st.text_input("Área de conocimiento", value="Computación")
        with col3:
            disciplina = st.text_input("Disciplina", value="Ciencias de la Computación")
            area_unesco = st.text_input("Área UNESCO", value="Tecnologías de la Información y Comunicación")
            disciplina_unesco = st.text_input("Disciplina UNESCO", value="Tecnologías de la Información y la Comunicación")
            stem_micitt = st.text_input("¿STEM (MICITT)?", value="STEM")
        enviar_matricula = st.form_submit_button("Predecir matriculados")
    if enviar_matricula:
        payload = {
            "AÑO": anio,
            "UNIVERSIDAD": universidad,
            "CARRERA": carrera_m,
            "REGION_PLANIFICACION_SEDE": region_planificacion_sede,
            "GAM_SEDE": gam_sede,
            "GRADO_ACADEMICO": grado_academico,
            "NIVEL_ACADEMICO": nivel_academico,
            "NIVEL_CINE": nivel_cine,
            "AREA_CONOCIMIENTO": area_conocimiento,
            "DISCIPLINA": disciplina,
            "AREA_UNESCO": area_unesco,
            "DISCIPLINA_UNESCO": disciplina_unesco,
            "STEM_MICITT": stem_micitt}
        try:
            r = requests.post(f"{API_URL}/predecir/matriculados", json=payload, timeout=10)
            r.raise_for_status()
            resultado = r.json()
            st.metric("Matriculados predichos", resultado["matriculados_predicho"])
        except requests.RequestException as e:
            st.error(f"Error al consultar la API: {e}")