from __future__ import print_function
import os.path
import os
import pickle
from generarToken import generar_token
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# --- Alcances (permisos) que queremos ---
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets.readonly",
    "https://www.googleapis.com/auth/drive.readonly"]
TOKEN_PATH = r"C:\Users\Laura\Desktop\Data Scientist\Ejercicios Google Drive\secrets\token.json"
CREDENTIALS_PATH = r"C:\Users\Laura\Desktop\Data Scientist\Ejercicios Google Drive\secrets\credentials.json"
RANGE_NAME= 'A10:Z80'

# --- Crear servicio de conexión con Google Drive ---
def crear_servicio():
    creds = None
    # Ruta absoluta para credentials.json (seguro que lo encuentra)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    credentials_path = os.path.join(current_dir, CREDENTIALS_PATH)

    # Revisamos si ya existe un token guardado
    if os.path.exists(TOKEN_PATH):
        print("Si existe el archivo")
        creds = Credentials.from_authorized_user_file(TOKEN_PATH , SCOPES)
        print( creds)
    # Si no hay credenciales válidas, pedimos login
    else:
        if creds and creds.expired and creds.refresh_token:
            print("🔄 Renovando credenciales con refresh_token...")
            generar_token()
        else:
            generar_token()


    # Creamos el servicio de Drive
    service = build("drive", "v3", credentials=creds)
    print("✅ Conexión lista con Google Drive")
    return service


# --- EJECUCION #1 ---prpobando conección

drive_service = crear_servicio()
Spreedsheet_ID = "1_NlphFPPBWMmhDSyeBrInyaNq9oUb5Ds"
# Ejemplo: listar los primeros 10 archivos de tu Google Drive !!las primeros 10 archivos que estan en drive sin importar carpetas ni nada"
try:
    results = drive_service.files().list(
        pageSize=10, fields="files(id, name)"
    ).execute()
    items = results.get("files", [])

    if not items:
        print("No se encontraron archivos.")
    else:
        print("Archivos encontrados: EXITO!!")
        # for item in items:
        #     print(f"{item['name']} ({item['id']})")
except Exception as e:
    print("❌ Error al intentar listar archivos:")
    print(e)

print(""
"////////////////////////////////////////////////////////////////////////" \
"" \
"" \
""
)

def crear_serviciosheets():
    creds = Credentials.from_authorized_user_file(TOKEN_PATH, ["https://www.googleapis.com/auth/spreadsheets.readonly"])
    service = build("sheets", "v4", credentials=creds)
    return service
# Ejemplo: listar los archivos de una carpeta de Google Drive

folder_id = '13N0UeJYlTZQp29pwEQ3LrW_eC1GgDQc7'
#Verificamos que el archivo si sea google sheets para poder leer y editar
query = f"'{folder_id}' in parents and mimeType = 'application/vnd.google-apps.spreadsheet'"


results = drive_service.files().list(
    q=query,
    fields="files(id, name, mimeType)"
).execute()

maestrosFaltantes= []
faltantes = []


for item in results.get('files', []):
    SPREADSHEET_ID= item['id']
    print(f"{item['name']} ({item['id']})")
    service = crear_serviciosheets()
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=item['id'], range=RANGE_NAME).execute()
    values = result.get("values", [])
    
        # N'umero decolumna que estamos revisando
    for i, row in enumerate(values, start=10):
        
        col_index=6 
        # print(row)
        # print(i)  # fila real
        # print(col_index)
        # print(row[col_index].strip() ) ### Valor de la fila 10 columna 6 --- en la ultima vuelta cause error porque el indice no existe! en esta columnano hay nada
        # print(len(row))
        if not row or len(row) == 0 or not row[0] or str(row[0]).strip() == "":
            print("Ya se terminó de leer el archivo")
            faltantes.append("No termino")
            print("Aqui se agrega la frase "+ faltantes)
            break
        print(str(row[0]) == "")
        if  len(row)< col_index or str(row[0]).strip() == "" :
            if row[0].strip() == "":
                print("Ya se termino de leer el erchivo")
                faltantes = []
                break
            else:
                print("Este archivo esta vacio o no esta completo")
                faltantes.append("No termino")
                print(faltantes)
                break
        else:
            if  row[col_index].strip() == "" and row <26 :
                print("Este archivo no esta completamente lleno")
                faltantes.append("No termino")
                print ( "Faltante" + faltantes )
                break
            else:
                print("Esta celda si tiene valor, continuamos")
    print(faltantes)
    print(faltantes == "No termino")
    if faltantes == "No termino" :
        maestrosFaltantes.append(item['name'][:12])
    print(maestrosFaltantes)
    faltantes.clear()
    print(faltantes)


print(""
"////////////////////////////////////////////////////////////////////////" \
"" \
"" \
""
)


# Probar búsqueda de archivos en Drive !!TODOS los que estan en drive sin importar carpetas ni nada"
# if drive_service:
#     print("\n📂 Archivos en tu Drive:")
#     results = drive_service.files().list( fields="files(id, name)"
#     ).execute()
#     items = results.get("files", [])
#     for item in items:
#         print(f"- {item['name']} ({item['id']})")

print("Next step")

from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from datetime import datetime, timedelta
import pandas as pd
from twilio.rest import Client

# --- CONFIGURACIÓN --- # Ajusta rango según tu archivo


# Relación Mes -> Columna
COLUMNAS_MESES = {
    1: 1,  2: 2,  3: 3,  4: 4,  5: 5,  6: 6,
    7: 7,  8: 8,  9: 9,  10: 10, 11: 11, 12: 12
}

# --- FUNCIONES ---

def es_ultimo_tres_dias_habiles():
    hoy = datetime.now().date()
    print(hoy)
    fin_mes = (hoy.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)
    print(fin_mes)
    print(timedelta(days=1))

    # últimos 3 hábiles
    dias_habiles = []
    dia = fin_mes
    while len(dias_habiles) < 15: # Este numero indica cuantos dias habiles antes de fin demes
        if dia.weekday() < 5:  # 0=lunes, 6=domingo
            dias_habiles.append(dia)
        dia -= timedelta(days=1)

    print (dias_habiles)
    return hoy in dias_habiles

# -------------------------------------------------------------------------------

# Twilio config (cambia estos valores por los de tu cuenta)
TWILIO_ACCOUNT_SID = 'AC55b48635d08a0c34ca8679ccf6c6ab7c'
TWILIO_AUTH_TOKEN = '[AuthToken]'
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN )
TWILIO_WHATSAPP = "whatsapp:+14155238886"  # número oficial Twilio sandbox
MI_WHATSAPP = "whatsapp:+5215623672099"     # tu número de WhatsApp con código de país

print( "Enviar whats app")

from twilio.rest import Client

account_sid = 'AC55b48635d08a0c34ca8679ccf6c6ab7c'
auth_token = '378eca1211be59fcaa747714f178d382'
client = Client(account_sid, auth_token)



def enviar_whatsapp(mensaje):

    if maestrosFaltantes != "" :
        message = client.messages.create(
            from_='whatsapp:+14155238886',  # Este es el número del sandbox
            body=f'Hola Maestro, ya se revisaron los archivos de la carpeta tal y los siguientes profes {maestrosFaltantes} no han entregado aún 😄, hagamos seguimiento para saber que paso!',
            to='whatsapp:+5215623672099'  # Tu número de WhatsApp verificado
        )




def verificar_mes_actual():
    print("Revisando en que mes estamos")
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
    values = result.get("values", [])
    print ("Solo verifico que tengo datos en la hoja")

    if not values:
        return "⚠️ No se encontraron datos en la hoja."

    mes = datetime.now().month
    col_index = COLUMNAS_MESES[mes]
    print(mes)
    print(col_index)

    faltantes = []
    for i, row in enumerate(values, start=6):  # fila real
        if len(row) <= col_index or row[col_index].strip() == "":
            faltantes.append(i)

    if faltantes:
        return f"⚠️ Faltan datos en la columna del mes {mes} en filas: {faltantes}"
        print("⚠️ Faltan datos en la columna del mes {mes} en filas: {faltantes}")
    else:
        return f"✅ La columna del mes {mes} está completa."
        print("✅ La columna del mes {mes} está completa.")

# --- EJECUCION #3 ---

if es_ultimo_tres_dias_habiles():
    mensaje = verificar_mes_actual()
    print("Mensaje"+ mensaje)
    enviar_whatsapp(mensaje)
    print("📲 Notificación enviada:", mensaje)
else:
    print("Hoy no es uno de los últimos 3 días hábiles del mes.")
