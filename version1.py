import streamlit as st
import sqlite3
import pandas as pd

 # Conexión a bases de datos
conn_sesiones = sqlite3.connect("sesiones.db", check_same_thread=False)
cursor_sesiones = conn_sesiones.cursor()

conn_ejercicios = sqlite3.connect("ejercicios.db", check_same_thread=False)
cursor_ejercicios = conn_ejercicios.cursor()

 # Crear tablas si no existen
cursor_sesiones.execute('''
    CREATE TABLE IF NOT EXISTS sesiones (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fecha TEXT,
        tipo TEXT,
        estado TEXT
     )
 ''')
conn_sesiones.commit()

cursor_ejercicios.execute('''
     CREATE TABLE IF NOT EXISTS bloques (
         id INTEGER PRIMARY KEY AUTOINCREMENT,
         sesion_id INTEGER,
         tipo TEXT
     )
 ''')
conn_ejercicios.commit()

cursor_ejercicios.execute('''
     CREATE TABLE IF NOT EXISTS ejercicios (
         id INTEGER PRIMARY KEY AUTOINCREMENT,
         bloque_id INTEGER,
         ejercicio TEXT,
         categoria TEXT,
         subcategoria TEXT
     )
 ''')
conn_ejercicios.commit()

 # Estado de la sesión de Streamlit
if "sesion_temp" not in st.session_state:
     st.session_state.sesion_temp = {
         "nombre": "",
         "fecha": None,
         "bloques": []
     }
if "creando_sesion" not in st.session_state:
     st.session_state.creando_sesion = False
if "sesion_seleccionada" not in st.session_state:
     st.session_state.sesion_seleccionada = None

def obtener_lista_sesiones():
     return pd.read_sql("SELECT * FROM sesiones ORDER BY fecha DESC", conn_sesiones)

def obtener_lista_ejercicios():
     return pd.read_sql("SELECT DISTINCT categoria, subcategoria, ejercicio FROM ejercicios ORDER BY categoria, subcategoria, ejercicio", conn_ejercicios)

def obtener_bloques_y_ejercicios(sesion_id):
     bloques_df = pd.read_sql(f"SELECT * FROM bloques WHERE sesion_id = {sesion_id}", conn_ejercicios)
     bloques = []
     for _, bloque in bloques_df.iterrows():
         ejercicios_df = pd.read_sql(f"SELECT * FROM ejercicios WHERE bloque_id = {bloque['id']}", conn_ejercicios)
         bloques.append({"nombre": bloque["tipo"], "ejercicios": ejercicios_df.to_dict(orient="records")})
     return bloques

def mostrar_sesion_completa(sesion_id):
     sesion = pd.read_sql(f"SELECT * FROM sesiones WHERE id = {sesion_id}", conn_sesiones).iloc[0]
     bloques = obtener_bloques_y_ejercicios(sesion_id)
    
     st.header(f"📅 {sesion['fecha']} - {sesion['tipo']}")
    
     for bloque in bloques:
         with st.expander(f"🟢 {bloque['nombre']}", expanded=True):
             for ejercicio in bloque["ejercicios"]:
                 st.write(f"✅ {ejercicio['ejercicio']} ({ejercicio['categoria']} - {ejercicio['subcategoria']})")
    
     if st.button("⬅️ Volver a la lista de sesiones"):
         st.session_state.sesion_seleccionada = None
         st.rerun()

def agregar_sesion_temporal():
     if st.session_state.sesion_temp["nombre"] and st.session_state.sesion_temp["fecha"]:
         fecha_str = st.session_state.sesion_temp["fecha"].strftime("%Y-%m-%d")
         cursor_sesiones.execute(
             "INSERT INTO sesiones (fecha, tipo, estado) VALUES (?, ?, 'proxima')",
             (fecha_str, st.session_state.sesion_temp["nombre"])
         )
         conn_sesiones.commit()
         sesion_id = cursor_sesiones.lastrowid
        
         for bloque in st.session_state.sesion_temp["bloques"]:
             cursor_ejercicios.execute(
                 "INSERT INTO bloques (sesion_id, tipo) VALUES (?, ?)",
                 (sesion_id, bloque["nombre"])
             )
             bloque_id = cursor_ejercicios.lastrowid
            
             for ejercicio in bloque["ejercicios"]:
                 cursor_ejercicios.execute(
                     "INSERT INTO ejercicios (bloque_id, ejercicio, categoria, subcategoria) VALUES (?, ?, ?, ?)",
                     (bloque_id, ejercicio["nombre"], ejercicio["categoria"], ejercicio["subcategoria"])
                 )
         conn_ejercicios.commit()
         st.session_state.sesion_temp = {"nombre": "", "fecha": None, "bloques": []}
         st.session_state.creando_sesion = False
         st.success("✅ Sesión guardada correctamente")
         st.rerun()
     else:
         st.error("⚠️ Debes asignar un nombre y una fecha a la sesión")

def obtener_lista_sesiones():
     return pd.read_sql("SELECT * FROM sesiones ORDER BY fecha DESC", conn_sesiones)

def obtener_lista_ejercicios():
     return pd.read_sql("SELECT DISTINCT categoria, subcategoria, ejercicio FROM ejercicios ORDER BY categoria, subcategoria, ejercicio", conn_ejercicios)

def obtener_bloques_y_ejercicios(sesion_id):
     bloques_df = pd.read_sql(f"SELECT * FROM bloques WHERE sesion_id = {sesion_id}", conn_ejercicios)
     bloques = []
     for _, bloque in bloques_df.iterrows():
         ejercicios_df = pd.read_sql(f"SELECT * FROM ejercicios WHERE bloque_id = {bloque['id']}", conn_ejercicios)
         bloques.append({"nombre": bloque["tipo"], "ejercicios": ejercicios_df.to_dict(orient="records")})
     return bloques

st.title("📋 Planificador de Entrenamientos")

st.sidebar.header("📋 Sesiones")
if st.sidebar.button("➕ Crear Nueva Sesión"):
     st.session_state.creando_sesion = True
     st.session_state.sesion_seleccionada = None
     st.rerun()

pagina = st.sidebar.radio("Selecciona una opción", ["Próximas Sesiones", "Sesiones Pasadas"])

 # Mostrar las sesiones guardadas al inicio
if not st.session_state.creando_sesion and not st.session_state.sesion_seleccionada:
     sesiones_df = obtener_lista_sesiones()
     if not sesiones_df.empty:
         st.header("📅 Sesiones Guardadas")
         for _, sesion in sesiones_df.iterrows():
             if st.button(f"📅 {sesion['fecha']} - {sesion['tipo']}", key=f"sesion_{sesion['id']}"):
                 st.session_state.sesion_seleccionada = sesion['id']
                 st.rerun()
     else:
         st.info("No hay sesiones creadas.")

if st.session_state.sesion_seleccionada:
     mostrar_sesion_completa(st.session_state.sesion_seleccionada)

if st.session_state.creando_sesion:
     st.header("📅 Crear Nueva Sesión")
     if st.button("⬅️ Volver atrás"):
         st.session_state.creando_sesion = False
         st.rerun()
    
     st.session_state.sesion_temp["nombre"] = st.text_input("Nombre de la sesión", value=st.session_state.sesion_temp["nombre"])
     st.session_state.sesion_temp["fecha"] = st.date_input("Fecha de la sesión", value=pd.to_datetime("today"))
    
     st.subheader("Añadir Bloques")
     tipo_bloque = st.selectbox("Tipo de Bloque", ["Calentamiento", "Circuito", "Superset"], key=f"nuevo_bloque_{len(st.session_state.sesion_temp['bloques'])}")
     if st.button("Añadir Bloque"):
         st.session_state.sesion_temp["bloques"].append({"nombre": tipo_bloque, "ejercicios": []})
         st.rerun()
    
     for i, bloque in enumerate(st.session_state.sesion_temp["bloques"]):
         with st.expander(f"🟢 {bloque['nombre']}"):
             st.write("### Ejercicios en este bloque:")
             for ejercicio in bloque["ejercicios"]:
                 st.write(f"✅ {ejercicio['nombre']} ({ejercicio['categoria']} - {ejercicio['subcategoria']})")
            
             lista_ejercicios_df = obtener_lista_ejercicios()
             categoria_opciones = lista_ejercicios_df["categoria"].dropna().unique().tolist()
             categoria_seleccionada = st.selectbox("Categoría", categoria_opciones, key=f"categoria_{i}")
            
             subcategoria_df = lista_ejercicios_df[lista_ejercicios_df["categoria"] == categoria_seleccionada]
             subcategoria_opciones = subcategoria_df["subcategoria"].dropna().unique().tolist()
             subcategoria_seleccionada = st.selectbox("Subcategoría", subcategoria_opciones, key=f"subcategoria_{i}")
            
             ejercicio_df = subcategoria_df[subcategoria_df["subcategoria"] == subcategoria_seleccionada]
             ejercicio_opciones = ejercicio_df["ejercicio"].dropna().unique().tolist()
             nombre_ejercicio = st.selectbox("Ejercicio", ejercicio_opciones, key=f"ejercicio_{i}")
            
             if st.button("Añadir Ejercicio", key=f"btn_ejercicio_{i}"):
                 st.session_state.sesion_temp["bloques"][i]["ejercicios"].append({
                     "nombre": nombre_ejercicio,
                     "categoria": categoria_seleccionada,
                     "subcategoria": subcategoria_seleccionada
                 })
                 st.rerun()
                
     if st.button("💾 Guardar Sesión"):
         agregar_sesion_temporal()
