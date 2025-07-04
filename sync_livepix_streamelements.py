import os
import requests

# --- Configurações via variáveis de ambiente ---
LIVEPIX_CLIENT_ID = os.getenv('LIVEPIX_CLIENT_ID')
LIVEPIX_CLIENT_SECRET = os.getenv('LIVEPIX_CLIENT_SECRET')

if not all([LIVEPIX_CLIENT_ID, LIVEPIX_CLIENT_SECRET]):
    raise Exception("Por favor configure as variáveis de ambiente LIVEPIX_CLIENT_ID e LIVEPIX_CLIENT_SECRET.")

# --- Obter access token do LivePix (OAuth2) ---
def get_livepix_token():
    url = "https://oauth.livepix.gg/oauth2/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "client_credentials",
        "client_id": LIVEPIX_CLIENT_ID,
        "client_secret": LIVEPIX_CLIENT_SECRET,
        "scope": "wallet:read"
    }
    response = requests.post(url, headers=headers, data=data)
    if response.status_code != 200:
        print("Status code:", response.status_code)
        print("Resposta da API:", response.text)
        response.raise_for_status()
    token_data = response.json()
    print("Token data completa:", token_data)
    return token_data["access_token"]

# --- Consultar saldo da carteira LivePix ---
def get_livepix_balance(access_token):
    url = "https://api.livepix.gg/v2/wallet"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()
    data_list = data.get("data", [])
    if data_list and isinstance(data_list, list):
        balance = data_list[0].get("balance", 0)
    else:
        balance = 0
    return balance

def main():
    try:
        # 1) Obter token OAuth2 LivePix
        token = get_livepix_token()
        print("Token LivePix obtido com sucesso.")

        # 2) Consultar saldo
        balance = get_livepix_balance(token)

        # Formatar o saldo em formato monetário brasileiro
        balance_formatted = f"R$ {balance:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        print(f"Saldo LivePix: {balance_formatted}")

    except Exception as e:
        print("Erro durante a sincronização:", e)

if __name__ == "__main__":
    main()
