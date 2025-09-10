from __future__ import print_function
import os
import json
import pickle
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# 🔹 SCOPES: permisos que vamos a pedir (Drive + Sheets)
SCOPES = [
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/spreadsheets"
]

# 🔹 Rutas locales de credenciales
CREDENTIALS_PATH = r"c:\Users\Laura\Desktop\Data Scientist\Ejercicios Google Drive\Prepa57\credentials.json"
   # Tu archivo descargado de Google Cloud
TOKEN_PATH = r"c:\Users\Laura\Desktop\Data Scientist\Ejercicios Google Drive\Prepa57\token.json"              # Se genera al autorizar

def crear_servicio(api_name, api_version, scopes):
    creds = None

    # Si existe token.json y no está vacío → intentar cargar
    if os.path.exists(TOKEN_PATH) and os.path.getsize(TOKEN_PATH) > 0:
        try:
            creds = Credentials.from_authorized_user_file(TOKEN_PATH, scopes)
        except Exception as e:
            print("⚠️ Error leyendo token.json, se borrará:", e)
            os.remove(TOKEN_PATH)
            creds = None

    # Si no hay credenciales válidas, pedimos login
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("🔄 Renovando credenciales con refresh_token...")
            creds.refresh(Request())
        else:
            print("🔑 Abriendo navegador para autorización...")
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, scopes)
            creds = flow.run_local_server(port=8080)

        # Guardar token.json nuevo
        with open(TOKEN_PATH, "w") as token:
            token.write(creds.to_json())
            print("✅ Nuevo token.json guardado")

    # Crear servicio
    try:
        service = build(api_name, api_version, credentials=creds)
        print(f"✅ Servicio {api_name} {api_version} creado correctamente")
        return service
    except Exception as e:
        print("❌ Error al crear servicio:", e)
        return None


# ------------------ PRUEBA ------------------
if __name__ == "__main__":
    # Crear servicio Drive
    drive_service = crear_servicio("drive", "v3", SCOPES)

    # Crear servicio Sheets
    sheets_service = crear_servicio("sheets", "v4", SCOPES)

    # Probar búsqueda de archivos en Drive
    if drive_service:
        print("\n📂 Archivos en tu Drive:")
        results = drive_service.files().list(
            pageSize=5, fields="files(id, name)"
        ).execute()
        items = results.get("files", [])
        for item in items:
            print(f"- {item['name']} ({item['id']})")

