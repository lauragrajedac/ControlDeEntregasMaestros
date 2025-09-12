import schedule
import subprocess
from schedule import repeat, every
import time


@repeat(every(5).seconds, texto="5 segundos")

def trabajo_programado(texto):
    print(f'Se ejecuto correctamente el codigo {texto}')

while True:
    schedule.run_pending()
    time.sleep(5)



# Ruta al script que quieres ejecutar
script_a_ejecutar = r"C:\Users\Laura\Desktop\Data Scientist\Ejercicios Google Drive\Prepa57\chaty.py"

# Ejecuta el script y captura la salida
resultado = subprocess.run(["python", script_a_ejecutar], capture_output=True, text=True)

# Imprime la salida estándar y los errores (si los hay)
print("Salida estándar:", resultado.stdout)
print("Errores:", resultado.stderr)