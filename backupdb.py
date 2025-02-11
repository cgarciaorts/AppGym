import shutil

shutil.copy("sesiones.db", "sesiones_backup.db")
shutil.copy("ejercicios.db", "ejercicios_backup.db")

print("✅ Copia de seguridad realizada.")
