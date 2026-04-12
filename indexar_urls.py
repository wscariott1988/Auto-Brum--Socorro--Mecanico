import json
import os
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Configurações solicitadas
SERVICE_ACCOUNT_FILE = 'credenciais.json.json'
SCOPES = ['https://www.googleapis.com/auth/indexing']
BASE_URL = 'https://www.mecanicaautobrum.com.br'

# Lista das 4 novas landing pages
urls_to_index = [
    f"{BASE_URL}/novo-hamburgo",
    f"{BASE_URL}/sao-leopoldo",
    f"{BASE_URL}/campo-bom",
    f"{BASE_URL}/estancia-velha"
]

def indexar_urls():
    if not os.path.exists(SERVICE_ACCOUNT_FILE):
        print(f"ERRO: Arquivo {SERVICE_ACCOUNT_FILE} não encontrado na raiz.")
        return

    # Autenticação via Service Account
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    
    # Inicializa a Indexing API v3
    service = build('indexing', 'v3', credentials=credentials)

    for url in urls_to_index:
        print(f"Solicitando indexação para: {url}")
        
        body = {
            "url": url,
            "type": "URL_UPDATED"
        }
        
        try:
            # Envio da solicitação
            response = service.urlNotifications().publish(body=body).execute()
            print(f"SUCESSO: {url} | Resposta: {response}")
        except Exception as e:
            print(f"ERRO ao indexar {url}: {e}")

if __name__ == "__main__":
    print("--- INICIANDO INTEGRAÇÃO GOOGLE INDEXING API ---")
    indexar_urls()
    print("--- PROCESSO CONCLUÍDO ---")
