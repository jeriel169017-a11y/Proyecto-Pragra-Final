import os
import requests
import streamlit as st
import pandas as pd
import pydeck as pdk
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
        st.error("No se pudo conectar a la API")
    elif not estado.get("modelos_cargados"):
        st.warning("La API responde, pero los modelos aún no están entrenados/cargados")
    else:
        st.success("API conectada y modelos listos")
# Datos geográficos para la pestaña "Mapa" (punto extra)
COORDENADAS_PROVINCIAS = { # Coordenadas aproximadas del centro de cada provincia de Costa Rica
    "San José": (9.9281, -84.0907),
    "Alajuela": (10.0162, -84.2116),
    "Cartago": (9.8644, -83.9194),
    "Heredia": (10.0024, -84.1165),
    "Guanacaste": (10.6333, -85.4333),
    "Puntarenas": (9.9762, -84.8384),
    "Limón": (9.9908, -83.0356)}
# Coordenadas aproximadas de sedes/recintos de la UCR
# La clave es una palabra que se busca dentro de lo que el usuario escriba en "Sede"
COORDENADAS_SEDES = {
    "RODRIGO FACIO": ("Sede Rodrigo Facio (San Pedro, San José)", 9.9367, -84.0508),
    "OCCIDENTE": ("Sede de Occidente (San Ramón, Alajuela)", 10.0904, -84.4757),
    "ATLANTICO": ("Sede del Atlántico (Turrialba, Cartago)", 9.9037, -83.6828),
    "ATLÁNTICO": ("Sede del Atlántico (Turrialba, Cartago)", 9.9037, -83.6828),
    "PACIFICO": ("Sede del Pacífico (Puntarenas)", 9.9763, -84.8384),
    "PACÍFICO": ("Sede del Pacífico (Puntarenas)", 9.9763, -84.8384),
    "GUANACASTE": ("Sede de Guanacaste (Liberia)", 10.6346, -85.4370),
    "CARIBE": ("Sede del Caribe (Limón)", 9.9908, -83.0356),
    "GOLFITO": ("Recinto de Golfito", 8.6415, -83.1554),
    "PARAISO": ("Recinto de Paraíso (Cartago)", 9.8419, -83.8524),
    "PARAÍSO": ("Recinto de Paraíso (Cartago)", 9.8419, -83.8524),
    "TACARES": ("Recinto de Tacares (Grecia)", 10.0743, -84.3130),
    "GRECIA": ("Recinto de Grecia", 10.0743, -84.3130)}
"Busca en COORDENADAS_SEDES una palabra clave contenida en el texto que escribió el usuario"
def buscar_sede(texto_sede):
    texto_upper = texto_sede.upper()
    for clave, (nombre, lat, lon) in COORDENADAS_SEDES.items():
        if clave in texto_upper:
            return nombre, lat, lon
    return None
tab_admision, tab_matricula, tab_mapa = st.tabs(
    ["Rango de nota de admisión", "Demanda de matrícula", "Mapa"])
# Parte 1: Clasificación - Rango_Nota_Admision
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
            # guardamos la predicción para poder mostrarla en la pestaña Mapa
            st.session_state["prediccion_nota"] = {
                "provincia_residencia": provincia_residencia,
                "sede": sede,
                "resultado": resultado["rango_nota_admision_predicho"],
            }
        except requests.RequestException as e:
            st.error(f"Error al consultar la API: {e}")
# Parte 2: Regresión - Matriculados
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
# Parte 3: Mapa (visualización adicional - punto extra)
with tab_mapa:
    st.subheader("Ubicación geográfica de la predicción")
    if "prediccion_nota" not in st.session_state:
        st.info("Todavía no hay ninguna predicción hecha, realiza alguna")
    else:
        pred = st.session_state["prediccion_nota"]
        st.write(
            "Mapa de la última predicción realizada: dónde vive el estudiante "
            "y en qué sede de la UCR va a estudiar, con el resultado obtenido de la API")
        puntos = []
        # Provincia de residencia -> punto azul
        if pred["provincia_residencia"] in COORDENADAS_PROVINCIAS:
            lat, lon = COORDENADAS_PROVINCIAS[pred["provincia_residencia"]]
            puntos.append({
                "lat": lat, "lon": lon,
                "etiqueta": "🏠 Vive aquí: " + pred["provincia_residencia"],
                "color": [0, 102, 204]})   # Azul
        # Sede donde va a estudiar
        sede_encontrada = buscar_sede(pred["sede"])
        if sede_encontrada:
            nombre_sede, lat, lon = sede_encontrada
            puntos.append({
                "lat": lat, "lon": lon,
                "etiqueta": "🎓 Estudia aquí: " + nombre_sede,
                "color": [0, 153, 76]})   # Verde
        if puntos:
            df_mapa = pd.DataFrame(puntos)
            # Círculos de colores: radius_min/max_pixels fija el tamaño EN PANTALLA
            # (no en metros del mapa), así no se ven gigantes al hacer zoom o acercarse
            capa_puntos = pdk.Layer(
                "ScatterplotLayer",
                data=df_mapa,
                get_position=["lon", "lat"],
                get_fill_color="color",
                get_radius=1,
                radius_min_pixels=6,
                radius_max_pixels=10,
                pickable=True)
            # Etiqueta de texto sobre cada punto
            capa_texto = pdk.Layer(
                "TextLayer",
                data=df_mapa,
                get_position=["lon", "lat"],
                get_text="etiqueta",
                get_size=14,
                get_color=[0, 0, 0],
                get_alignment_baseline="'bottom'",
                get_pixel_offset=[0, -12])
            vista = pdk.ViewState(
                latitude=df_mapa["lat"].mean(),
                longitude=df_mapa["lon"].mean(),
                zoom=7)
            st.pydeck_chart(pdk.Deck(
                layers=[capa_puntos, capa_texto],
                initial_view_state=vista,
                map_style=None,
                tooltip={"text": "{etiqueta}"}))
            for p in puntos:
                st.caption(p["etiqueta"])
            st.success("Rango de nota predicho: " + str(pred["resultado"]))
        else:
            st.warning(
                "No se reconoce ni la provincia ni la sede escritas en el formulario. "
                "Provincias válidas: " + ", ".join(COORDENADAS_PROVINCIAS.keys()) +
                ". Sedes válidas (basta con que el texto de 'Sede' contenga una de estas "
                "palabras): " + ", ".join(sorted(set(v[0].split(" (")[0] for v in COORDENADAS_SEDES.values()))))