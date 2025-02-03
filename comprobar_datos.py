import sqlite3

# Conectar a la base de datos
conn = sqlite3.connect("ejercicios.db")
cursor = conn.cursor()

# Contar cuántos registros hay en la tabla ejercicios
cursor.execute("SELECT COUNT(*) FROM ejercicios")
cantidad = cursor.fetchone()[0]

if cantidad > 0:
    print(f"✅ La tabla ejercicios tiene {cantidad} registros.")
else:
    print("⚠ La tabla ejercicios está vacía.")

# Cerrar la conexión
conn.close()
