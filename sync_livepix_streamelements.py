import os
import requests

# --- Configurações via variáveis de ambiente ---
LIVEPIX_CLIENT_ID = os.getenv('LIVEPIX_CLIENT_ID')
LIVEPIX_CLIENT_SECRET = os.getenv('LIVEPIX_CLIENT_SECRET')
STREAMELEMENTS_TOKEN = os.getenv('STREAMELEMENTS_TOKEN')
STREAMELEMENTS_CHANNEL_ID = os.getenv('STREAMELEMENTS_CHANNEL_ID')
STREAMELEMENTS_COUNTER_ID = os.getenv('STREAMELEMENTS_COUNTER_ID')

if not all([
    LIVEPIX_CLIENT_ID,
    LIVEPIX_CLIENT_SECRET,
    STREAMELEMENTS_TOKEN,
    STREAMELEMENTS_CHANNEL_ID,
    STREAMELEMENTS_COUNTER_ID
]):
    raise Exception("Por favor configure todas as variáveis de ambiente necessárias.")

# --- Obter access token do LivePix (OAuth2) ---
def get_livepix_token():
    url = "https://api.livepix.gg/v1/oauth2/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "client_credentials",
        "client_id": LIVEPIX_CLIENT_ID,
        "client_secret": LIVEPIX_CLIENT_SECRET
    }
    response = requests.post(url, headers=headers, data=data)
    response.raise_for_status()
    token_data = response.json()
    return token_data["access_token"]

# --- Consultar saldo da carteira LivePix ---
def get_livepix_balance(access_token):
    url = "https://api.livepix.gg/v1/wallet/balance"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()
    # Ajuste conforme estrutura real do JSON retornado pela API
    balance = data.get("data", {}).get("balance", 0)
    return balance

# --- Atualizar contador no StreamElements ---
def update_streamelements_counter(value):
    url = f"https://api.streamelements.com/kappa/v2/channels/{STREAMELEMENTS_CHANNEL_ID}/overlays/counters/{STREAMELEMENTS_COUNTER_ID}"
    headers = {
        "Authorization": f"Bearer {STREAMELEMENTS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "value": value
    }
    response = requests.put(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()

def main():
    try:
        # 1) Obter token OAuth2 LivePix
        token = get_livepix_token()
        print("Token LivePix obtido com sucesso.")

        # 2) Consultar saldo
        balance = get_livepix_balance(token)
        print(f"Saldo LivePix: {balance}")

        # 3) Atualizar contador StreamElements
        result = update_streamelements_counter(balance)
        print("Contador StreamElements atualizado:", result)

    except Exception as e:
        print("Erro durante a sincronização:", e)

if __name__ == "__main__":
    main()
