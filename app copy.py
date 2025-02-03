# import streamlit as st
# import sqlite3
# import pandas as pd

# # 📌 Configurar la base de datos
# conn = sqlite3.connect("sesiones.db", check_same_thread=False)
# cursor = conn.cursor()

# # 📌 Crear tablas si no existen
# cursor.execute("""
# CREATE TABLE IF NOT EXISTS sesiones (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     fecha TEXT,
#     tipo TEXT
# )
# """)

# cursor.execute("""
# CREATE TABLE IF NOT EXISTS ejercicios (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     ejercicio TEXT,
#     series INTEGER,
#     repeticiones TEXT,
#     explicacion TEXT,
#     rpe TEXT,
#     carga INTEGER,
#     categoria TEXT,
#     subcategoria TEXT
# )
# """)
# conn.commit()

# # 📌 Configurar la interfaz de la app
# st.set_page_config(page_title="Gestor de Sesiones", page_icon="⚡", layout="wide")

# # 📌 Título principal
# st.title("🏋️‍♂️ Gestor de Sesiones de Entrenamiento")

# # 📌 Menú de opciones
# menu = st.sidebar.radio("Selecciona una opción:", ["Próximas Sesiones", "Sesiones Pasadas"])

# # ------------------------------------
# # 🔥 FUNCIÓN PARA AÑADIR UNA SESIÓN
# # ------------------------------------
# def agregar_sesion():
#     with st.form("form_sesion"):
#         fecha = st.date_input("📅 Fecha de la sesión")
#         tipo = st.text_input("🏋️‍♂️ Tipo de sesión", placeholder="Ej. Fuerza, Cardio...")
#         enviar = st.form_submit_button("Guardar Sesión")

#         if enviar and fecha and tipo:
#             cursor.execute("INSERT INTO sesiones (fecha, tipo) VALUES (?, ?)", (fecha, tipo))
#             conn.commit()
#             st.success(f"✅ Sesión '{tipo}' añadida con éxito!")
#             st.rerun()

# # ------------------------------------
# # 🔥 FUNCIÓN PARA MOSTRAR SESIONES Y AGREGAR EJERCICIOS
# # ------------------------------------
# def mostrar_sesiones(filtro):
#     sesiones = pd.read_sql(f"SELECT * FROM sesiones WHERE fecha {filtro} DATE('now') ORDER BY fecha DESC", conn)
    
#     if sesiones.empty:
#         st.warning("No hay sesiones registradas.")
#         return
    
#     for _, row in sesiones.iterrows():
#         with st.expander(f"📅 {row['fecha']} - {row['tipo']}"):
#             ejercicios = pd.read_sql(f"SELECT * FROM ejercicios WHERE sesion_id = {row['id']}", conn)

#             if not ejercicios.empty:
#                 for _, e in ejercicios.iterrows():
#                     st.write(f"- {e['ejercicio']}: {e['descripcion']}")
#             else:
#                 st.info("No hay ejercicios en esta sesión.")

#             # Agregar ejercicios a la sesión
#             with st.form(f"form_ejercicio_{row['id']}"):
#                 ejercicio = st.text_input("🏋️‍♂️ Nombre del ejercicio", key=f"ej_{row['id']}")
#                 descripcion = st.text_area("📄 Descripción", key=f"desc_{row['id']}")
#                 enviar_ej = st.form_submit_button("➕ Agregar Ejercicio")

#                 if enviar_ej and ejercicio:
#                     cursor.execute("INSERT INTO ejercicios (sesion_id, ejercicio, descripcion) VALUES (?, ?, ?)", 
#                                    (row["id"], ejercicio, descripcion))
#                     conn.commit()
#                     st.success(f"✅ Ejercicio '{ejercicio}' añadido a la sesión.")
#                     st.rerun()

# # ------------------------------------
# # 📌 MOSTRAR PRÓXIMAS SESIONES
# # ------------------------------------
# if menu == "Próximas Sesiones":
#     st.header("📅 Próximas Sesiones")
#     if st.button("➕ Añadir Nueva Sesión"):
#         agregar_sesion()
#     mostrar_sesiones(">=")

# # ------------------------------------
# # 📌 MOSTRAR SESIONES PASADAS
# # ------------------------------------
# elif menu == "Sesiones Pasadas":
#     st.header("📜 Sesiones Pasadas")
#     mostrar_sesiones("<")