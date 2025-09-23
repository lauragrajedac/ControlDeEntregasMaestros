from __future__ import print_function
import os.path
import os
from generarToken import generar_token
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# --- Alcances (permisos) que queremos ---
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets.readonly",
    "https://www.googleapis.com/auth/drive.readonly"]
TOKEN_PATH = r" add your own path"
CREDENTIALS_PATH = r" add your own path"
RANGE_NAME= 'A10:Z80'

# --- Crear servicio de conexión con Google Drive ---
def crear_servicio():
    creds = None

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
# Verificando que esta leyendo nuestra carpeta drive correctamente
try:
    results = drive_service.files().list(
        pageSize=10, fields="files(id, name)"
    ).execute()
    items = results.get("files", [])

    if not items:
        print("No se encontraron archivos.")
    else:
        print("Archivos encontrados. EXITO!!")
        # for item in items:
        #     print(f"{item['name']} ({item['id']})")
except Exception as e:
    print("❌ Error al intentar listar archivos:")
    print(e)


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

def funcionQueRevisaInfo():
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
            
            col_index=7

            if not row or len(row) == 0 or not row[0] :

                fila_anterior =  i - 1
                if not row or not row[0] :
                        if not row :
                            faltantes.append("No termino")
                            print("no hay archivo")
                        elif not row[0]:
                            if i > 10:
                                fila_anterior = values[i - 11]
                                print(len(fila_anterior) > col_index)
                                print(len(row) < col_index)
                                print(fila_anterior[col_index].strip() != "")
                                if (len(fila_anterior) > col_index and len(row) < col_index and fila_anterior[col_index].strip() != ""):
                                    print("Aquí termina la primera tabla")
                                    break
                                elif (len(fila_anterior) > col_index and fila_anterior[col_index].strip() != ""):
                                    print("Aquí termina la primera tabla, pero agregaron totales al final")
                                    break
                                elif len(row) <= col_index:
                                    print("en este caso también termina pero parece ser que no inició")
                                    faltantes.append("No termino")
                                    
            else:
                print("Esta celda si tiene valor, continuamos")
            
            print("No termino" in faltantes)
            if  "No termino" in faltantes :
                maestrosFaltantes.append(item['name'][:12])
                print("hubo un faltante")
                print(maestrosFaltantes)
                faltantes.clear()
                print(faltantes)
                break
        
    print(maestrosFaltantes)
    print(not maestrosFaltantes)
    return maestrosFaltantes


from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from datetime import datetime, timedelta
from twilio.rest import Client

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
    while len(dias_habiles) < 3: # Este numero indica cuantos dias habiles antes de fin demes
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

from twilio.rest import Client

account_sid = 'AC55b48635d08a0c34ca8679ccf6c6ab7c'
auth_token = 'ceda262f53d1facfe3a80c063b9ad423'
client = Client(account_sid, auth_token)


def enviar_whatsapp(maestrosFaltantes):
    print(maestrosFaltantes)
    print( maestrosFaltantes != "" )
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
        print(col_index)
        if len(row) <= col_index or row[col_index].strip() == "":
            faltantes.append(i)

    if faltantes:        
        print("⚠️ Faltan datos en la columna del mes {mes} en filas: {faltantes}")
        return f"⚠️ Faltan datos en la columna del mes {mes} en filas: {faltantes}"
    else:
        print("✅ La columna del mes {mes} está completa.")
        return f"✅ La columna del mes {mes} está completa."

# --- EJECUCION #3 ---
def mandarMensaje ():
    if es_ultimo_tres_dias_habiles():
        mensaje = funcionQueRevisaInfo()
        lista_maestros = ", ".join(str(item) for item in mensaje)
        print("Estos maestros no han entregado aún"+  lista_maestros)
        print("Hora de mandar el mensaje por wha")
        enviar_whatsapp(lista_maestros)
        print("📲 Notificación enviada al director con los sig nombres: ", lista_maestros)
    else:
        print("Hoy no es uno de los últimos 3 días hábiles del mes.")
