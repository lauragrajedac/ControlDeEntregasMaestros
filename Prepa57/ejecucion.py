import schedule
from schedule import repeat, every
import time
from chaty import *
import pytz

# Get the complete list of timezones
# all_timezones_list = pytz.all_timezones
# print(len(all_timezones_list)) # Prints the number of timezones
# print(all_timezones_list[:596]) # Prints the first 10 timezones for example


def trabajo_programado(text):
    crear_servicio()
    mandarMensaje ()
    print(f'Se ejecuto correctamente el codigo {text}')


# every().day.at("17:55", "Mexico/General").do(trabajo_programado,text =" 💌 Ya se revisaron los archivos")
every().minute.do(trabajo_programado,text =" 💌 Ya se revisaron los archivos")

while True:
    schedule.run_pending()
    time.sleep(10)

