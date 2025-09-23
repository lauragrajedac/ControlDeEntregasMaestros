from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
import os

# Archivos
CREDENTIALS_PATH = r" add your own path"   # tu archivo descargado de Google Cloud
TOKEN_PATH = r" add your own path"         # aquí se guardará el token
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets.readonly",
    "https://www.googleapis.com/auth/drive.readonly"
]

def generar_token():
    if not os.path.exists(CREDENTIALS_PATH):
        raise FileNotFoundError(f"No se encontró {CREDENTIALS_PATH}")
    else:
        if not os.path.exists(TOKEN_PATH):
            # Forzar login con refresh_token válido
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_PATH, SCOPES
            )
            creds = flow.run_local_server(port=8080, access_type="offline", prompt="consent")

            # Guardar token.json limpio
            with open(TOKEN_PATH, "w") as token:
                token.write(creds.to_json())

            print(f"✅ Token generado correctamente en {TOKEN_PATH}")
        else:
            print(" 🎉 Ya existe token")

if __name__ == "__main__":
    generar_token()
