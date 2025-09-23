import schedule
from schedule import every
import time
from functions import *

def trabajo_programado(text):
    crear_servicio()
    mandarMensaje ()
    print(f'Se ejecuto correctamente el codigo {text}')

every().day.do(trabajo_programado,text =" Phyton y ya se revisaron los archivos 💌")

while True:
    
    schedule.run_pending()
    # time.sleep(10)

