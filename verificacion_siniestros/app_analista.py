# =====================================================================
# LIBRERÍAS (Estructura de la aplicación web y analítica tabular)
# =====================================================================

# os (Operating System): Utilizado para escanear y localizar las carpetas y archivos en el disco local.
import os

# json (JavaScript Object Notation): Se encarga de deserializar los archivos JSON de los expedientes para leerlos.
import json

# streamlit (st): Framework que transforma este script de Python en una aplicación web interactiva en localhost.
import streamlit as st

# pandas (pd): Librería de analítica de datos utilizada para empaquetar la información en tablas avanzadas (DataFrames).
import pandas as pd

# Configuración técnica de la interfaz web: layout="wide" aprovecha todo el ancho horizontal de la pantalla del navegador.
st.set_page_config(page_title="Dashboard de Auditoría InsurTech", layout="wide")

# =====================================================================
# 1. CONFIGURACIÓN DE RUTAS ABSOLUTAS (Tus carpetas de trabajo de Windows)
# =====================================================================
CARPETA_INPUTS = r"C:\Users\Carlos\Documents\Curso_Analisis_Data_bootcamp_Upgrade_Hub\Redes_Neuronales\verificacion_siniestros\data\input_imagenes"
CARPETA_JSONS = r"C:\Users\Carlos\Documents\Curso_Analisis_Data_bootcamp_Upgrade_Hub\Redes_Neuronales\verificacion_siniestros\data\out_put_json"

# Títulos del encabezado principal de la aplicación web
st.title("📊 Cuadro de Mando de Auditoría y Control de Costes")
st.write("Verificación cruzada de presupuestos frente a evidencias de IA con firma de responsabilidad pericial.")
st.markdown("---")

# =====================================================================
# 2. MOTOR DE CAPTURA Y CONSOLIDACIÓN DEL HISTÓRICO EN TIEMPO REAL
# =====================================================================

# Verificamos si existe la carpeta física de resultados para evitar fallos de ejecución.
if not os.path.exists(CARPETA_JSONS):
    st.error(f"❌ No se encontró la carpeta de reportes en: {CARPETA_JSONS}")
else:
    # Listamos todos los archivos que tengan la extensión .json dentro de la carpeta out_put_json.
    archivos_json = [f for f in os.listdir(CARPETA_JSONS) if f.endswith(".json")]
    
    if len(archivos_json) == 0:
        st.warning("⚠️ No hay expedientes JSON procesados todavía en la carpeta de destino.")
    else:
        # historico_expedientes: Lista temporal en memoria RAM para empaquetar los datos estructurados.
        historico_expedientes = []
        
        # Recorremos cada archivo JSON descubierto en el disco duro.
        for archivo_nombre in archivos_json:
            ruta_c = os.path.join(CARPETA_JSONS, archivo_nombre)
            
            # Abrimos y leemos el archivo con codificación segura utf-8.
            with open(ruta_c, "r", encoding="utf-8") as file:
                data = json.load(file)
                
                # Calculamos el total de fotos contando los elementos dentro de las listas de los caminos A y B.
                fotos_a = len(data.get("camino_a_automatizado", []))
                fotos_b = len(data.get("camino_b_revision_danos", []))
                
                # Inyectamos una fila estructurada en nuestro histórico por cada archivo analizado.
                # Guardamos el objeto completo 'data' bajo la clave 'datos_crudos' para usar sus listas internas abajo.
                historico_expedientes.append({
                    "ID Siniestro": data.get("id_siniestro"),
                    "Matrícula": data.get("matricula_vehiculo"),
                    "Presupuesto (€)": float(data.get("importe_reparacion", 0.0)),
                    "Responsable": data.get("usuario_responsable", "No registrado"),
                    "Fotos Automatizadas": fotos_a,
                    "Fotos Peritaje": fotos_b,
                    "Total Fotos": fotos_a + fotos_b,
                    "datos_crudos": data
                })
        
        # pd.DataFrame: Transformamos la lista de diccionarios en una matriz indexada de Pandas (Tabla analítica).
        df_historico = pd.DataFrame(historico_expedientes)

        # =====================================================================
        # 3. CAPA DE INDICADORES MACROECONÓMICOS (KPIs Superiores)
        # =====================================================================
        st.subheader("📈 Reporte Ejecutivo Operativo y Financiero")
        # Dividimos la pantalla en 4 columnas simétricas.
        m1, m2, m3, m4 = st.columns(4)
        
        with m1:
            # Cuenta el número total de filas únicas de la tabla para saber cuántos siniestros hay.
            st.metric(label="Total Siniestros Auditados", value=len(df_historico))
        with m2:
            # .sum() suma de forma aritmética toda la columna económica en memoria RAM.
            coste_total = df_historico["Presupuesto (€)"].sum()
            st.metric(label="Coste Total de Reparaciones", value=f"{coste_total:,.2f} €")
        with m3:
            # Sumamos el total de las imágenes procesadas por el sistema.
            st.metric(label="Total Fotos Analizadas", value=int(df_historico["Total Fotos"].sum()))
        with m4:
            # .mean() calcula de forma automática la media aritmética o coste medio por coche taller.
            coste_medio = df_historico["Presupuesto (€)"].mean()
            st.metric(label="Presupuesto Medio por Siniestro", value=f"{coste_medio:,.2f} €")
            
        st.markdown("---")

        # =====================================================================
        # 4. COMPONENTES DE FILTRADO INTERACTIVO (Barra Lateral Izquierda)
        # =====================================================================
        st.sidebar.header("🔍 Filtros de Búsqueda")
        
        # text_input: Genera una caja de texto libre. .upper() normaliza la entrada para el motor de búsqueda.
        buscar_placa = st.sidebar.text_input("Escriba la Matrícula:").strip().upper()
        
        # selectbox: Genera un desplegable agregando una opción comodín "MOSTRAR TODOS" al inicio.
        opciones_siniestros = ["MOSTRAR TODOS"] + list(df_historico["ID Siniestro"].unique())
        seleccion_siniestro = st.sidebar.selectbox("Seleccione ID de Siniestro:", opciones_siniestros)
        
        # df_filtrado: Clonamos el marco de datos original para aplicar filtros sin alterar la base maestra.
        df_filtrado = df_historico.copy()
        
        # Lógica de aplicación de filtros cruzados sobre el clon de la tabla:
        if buscar_placa:
            # .str.contains verifica coincidencias parciales de caracteres en la columna Matrícula.
            df_filtrado = df_filtrado[df_filtrado["Matrícula"].str.contains(buscar_placa, na=False)]
        if seleccion_siniestro != "MOSTRAR TODOS":
            # Filtro exacto por coincidencia de ID de Siniestro.
            df_filtrado = df_filtrado[df_filtrado["ID Siniestro"] == seleccion_siniestro]

        # =====================================================================
        # 5. RENDERIZADO DEL INVENTARIO TABULAR DE EXPEDIENTES
        # =====================================================================
        st.subheader("📋 Inventario de Expedientes Activos")
        
        # .drop(columns=["datos_crudos"]) elimina la columna técnica de metadatos antes de pintar la tabla en la web.
        df_visual = df_filtrado.drop(columns=["datos_crudos"]).copy()
        # st.dataframe muestra la tabla de Pandas estilizada con barras de desplazamiento interactivas.
        st.dataframe(df_visual, use_container_width=True)
        
        st.markdown("---")
        
        # =====================================================================
        # 6. DESGLOSE MULTIMEDIA: VINCULACIÓN DINÁMICA DE IMÁGENES REALES
        # =====================================================================
        st.subheader("🖼️ Verificación de Evidencias vs Importes")
        
        # Recorremos únicamente las filas que sobrevivieron a los filtros aplicados arriba.
        for idx, fila in df_filtrado.iterrows():
            # Extraemos los datos crudos del objeto JSON original de la fila actual.
            expediente = fila["datos_crudos"]
            id_sin = expediente["id_siniestro"]
            presupuesto_sin = expediente["importe_reparacion"]
            responsable_sin = expediente.get("usuario_responsable", "PERITO_ASIGNADO")
            
            # st.expander: Crea una caja colapsable para cada siniestro mostrando ID, Matrícula y Presupuesto en el título.
            with st.expander(f"📦 Expediente: {id_sin} | Matrícula: {expediente['matricula_vehiculo']} | 💰 PRESUPUESTO: {presupuesto_sin:,.2f} €", expanded=True):
                
                # st.caption añade una línea de texto pequeña con la traza de autoría y firma digital del perito.
                st.caption(f"✍️ **Expediente firmado digitalmente por:** `{responsable_sin}`")
                
                # REGLA DE NEGOCIO EN CALIENTE: Alerta visual condicional para auditoría de fraudes económicos.
                if presupuesto_sin > 1000:
                    st.warning(f"⚠️ Alerta de Auditoría: Este expediente supera los 1.000 € ({presupuesto_sin:,.2f} €). Cruce el coste con las imágenes de daños en el Camino B.")
                else:
                    st.info(f"ℹ️ Nota de Auditoría: Importe estándar de reparación ({presupuesto_sin:,.2f} €).")
                
                # Dividimos el interior del expander en dos bloques verticales para clasificar las imágenes en pantalla.
                col_izq, col_der = st.columns(2)
                # Localizamos la subcarpeta física exacta en el input correspondiente a este siniestro.
                ruta_fotos_siniestro = os.path.join(CARPETA_INPUTS, id_sin)
                
                # --- VISUALIZACIÓN DEL CAMINO A ---
                with col_izq:
                    st.write("**🚗 Camino A: Validación del Vehículo (Tomas Generales)**")
                    if len(expediente["camino_a_automatizado"]) == 0:
                        st.info("Sin tomas generales aprobadas por YOLO.")
                    else:
                        # Recorremos las fotos listadas en el Camino A del JSON.
                        for foto in expediente["camino_a_automatizado"]:
                            n_foto = foto["archivo"]
                            # Vinculamos la referencia de texto con la ruta del disco duro.
                            r_foto = os.path.join(ruta_fotos_siniestro, n_foto)
                            
                            if os.path.exists(r_foto):
                                # st.image lee el archivo binario y lo proyecta en la pantalla del analista.
                                st.image(r_foto, caption=f"Archivo: {n_foto} | Confianza IA: {foto['confianza_ia']}", use_container_width=True)
                
                # --- VISUALIZACIÓN DEL CAMINO B ---
                with col_der:
                    st.write("**🔍 Camino B: Revisión del Golpe (Daños Detallados)**")
                    if len(expediente["camino_b_revision_danos"]) == 0:
                        st.success("¡Todo limpio! Sin evidencias registradas en Camino B.")
                    else:
                        # Recorremos las fotos listadas en el Camino B del JSON.
                        for foto in expediente["camino_b_revision_danos"]:
                            n_foto = foto["archivo"]
                            # Vinculamos de nuevo el texto del JSON a los píxeles reales del almacenamiento.
                            r_foto = os.path.join(ruta_fotos_siniestro, n_foto)
                            
                            if os.path.exists(r_foto):
                                st.image(r_foto, caption=f"Archivo: {n_foto} | Diagnóstico: {foto['analisis']}", use_container_width=True)