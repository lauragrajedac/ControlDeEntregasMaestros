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
SCOPES = ["https://www.googleapis.com/auth/drive"]


# --- Crear servicio de conexión con Google Drive ---
def crear_servicio():
    creds = None

    # Ruta absoluta para credentials.json (seguro que lo encuentra)
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    credentials_path = os.path.join(current_dir, r"c:\Users\Laura\Desktop\Data Scientist\Ejercicios Google Drive\secrets\credentials.json")

    # Revisamos si ya existe un token guardado
    if os.path.exists(r"c:\Users\Laura\Desktop\Data Scientist\Ejercicios Google Drive\secrets\token.json"):
        creds = Credentials.from_authorized_user_file(r"c:\Users\Laura\Desktop\Data Scientist\Ejercicios Google Drive\secrets\token.json" , SCOPES)
    print( creds)
    # Si no hay credenciales válidas, pedimos login
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("🔄 Renovando credenciales con refresh_token...")
            generar_token()
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            creds = flow.run_local_server(port=8080, access_type="offline", prompt="consent")
        # Guardamos el token para no pedir login cada vez
        with open(r"c:\Users\Laura\Desktop\Data Scientist\Ejercicios Google Drive\secrets\token.json" , "w") as token:
            token.write(creds.to_json())

    # Creamos el servicio de Drive
    service = build("drive", "v3", credentials=creds)
    print("✅ Conexión lista con Google Drive")
    return service


# --- EJECUCION #1 ---prpobando conección

drive_service = crear_servicio()

# Ejemplo: listar los primeros 10 archivos de tu Google Drive
results = drive_service.files().list( pageSize=10, fields="files(id, name)" ).execute()
items = results.get("files", [])

if not items:
    print("No se encontraron archivos.")
else:
    print("Archivos encontrados:")
    for item in items:
        print(f"{item['name']} ({item['id']})")


print("////////////////////////////////////////////////////////////////////////")


# Probar búsqueda de archivos en Drive
if drive_service:
    print("\n📂 Archivos en tu Drive:")
    results = drive_service.files().list(
        pageSize=5, fields="files(id, name)"
    ).execute()
    items = results.get("files", [])
    for item in items:
        print(f"- {item['name']} ({item['id']})")

print("Next step")
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from datetime import datetime, timedelta
import pandas as pd
from twilio.rest import Client

# --- CONFIGURACIÓN ---
SPREADSHEET_ID = "1mEtvBlE7k2pIX5epoLtxhdNLUJ1pWe-s"
RANGE_NAME = "Hoja1!A6:Z50"   # Ajusta rango según tu archivo
CREDENTIALS_PATH = "credentials.json"
TOKEN_PATH = "token.json"

# Twilio config (cambia estos valores por los de tu cuenta)
TWILIO_ACCOUNT_SID = 'AC55b48635d08a0c34ca8679ccf6c6ab7c'
TWILIO_AUTH_TOKEN = '[AuthToken]'
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN )
TWILIO_WHATSAPP = "whatsapp:+14155238886"  # número oficial Twilio sandbox
MI_WHATSAPP = "whatsapp:+5215623672099"     # tu número de WhatsApp con código de país

# Relación Mes -> Columna
COLUMNAS_MESES = {
    1: 1,  2: 2,  3: 3,  4: 4,  5: 5,  6: 6,
    7: 7,  8: 8,  9: 9,  10: 10, 11: 11, 12: 12
}

# --- FUNCIONES ---
def crear_servicio():
    creds = Credentials.from_authorized_user_file(TOKEN_PATH, ["https://www.googleapis.com/auth/spreadsheets.readonly"])
    service = build("sheets", "v4", credentials=creds)
    return service

def es_ultimo_tres_dias_habiles():
    hoy = datetime.now().date()
    fin_mes = (hoy.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)

    # últimos 3 hábiles
    dias_habiles = []
    dia = fin_mes
    while len(dias_habiles) < 3:
        if dia.weekday() < 5:  # 0=lunes, 6=domingo
            dias_habiles.append(dia)
        dia -= timedelta(days=1)

    return hoy in dias_habiles

def enviar_whatsapp(mensaje):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    client.messages.create(
        body=mensaje,
        from_=TWILIO_WHATSAPP,
        to=MI_WHATSAPP
    )

def verificar_mes_actual():
    service = crear_servicio()
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
    values = result.get("values", [])

    if not values:
        return "⚠️ No se encontraron datos en la hoja."

    mes = datetime.now().month
    col_index = COLUMNAS_MESES[mes]

    faltantes = []
    for i, row in enumerate(values, start=6):  # fila real
        if len(row) <= col_index or row[col_index].strip() == "":
            faltantes.append(i)

    if faltantes:
        return f"⚠️ Faltan datos en la columna del mes {mes} en filas: {faltantes}"
    else:
        return f"✅ La columna del mes {mes} está completa."

# --- EJECUCION #3 ---

if es_ultimo_tres_dias_habiles():
    mensaje = verificar_mes_actual()
    enviar_whatsapp(mensaje)
    print("📲 Notificación enviada:", mensaje)
else:
    print("Hoy no es uno de los últimos 3 días hábiles del mes.")
