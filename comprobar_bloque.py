import sqlite3

conn = sqlite3.connect("ejercicios.db")
cursor = conn.cursor()

# Ver estructura de la tabla
cursor.execute("PRAGMA table_info(ejercicios)")
columnas = cursor.fetchall()

print("Estructura de la tabla ejercicios:")
for columna in columnas:
    print(columna)

conn.close()
