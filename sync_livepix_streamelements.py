import os
import requests

# --- Configurações via variáveis de ambiente ---
LIVEPIX_TOKEN = os.getenv('LIVEPIX_TOKEN')
STREAMELEMENTS_TOKEN = os.getenv('STREAMELEMENTS_TOKEN')
STREAMELEMENTS_CHANNEL_ID = os.getenv('STREAMELEMENTS_CHANNEL_ID')  # ID do canal/streamer
STREAMELEMENTS_COUNTER_ID = os.getenv('STREAMELEMENTS_COUNTER_ID')  # ID do contador a atualizar

if not all([LIVEPIX_TOKEN, STREAMELEMENTS_TOKEN, STREAMELEMENTS_CHANNEL_ID, STREAMELEMENTS_COUNTER_ID]):
    raise Exception("Por favor configure todas as variáveis de ambiente necessárias.")

# --- Função para obter saldo LivePix ---
def get_livepix_balance():
    url = "https://api.livepix.gg/v2/wallet/BRL/transactions"  # Confirmar endpoint exato na doc LivePix
    headers = {
        "Authorization": f"Bearer {LIVEPIX_TOKEN}",
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()
    # Ajuste conforme estrutura da resposta real da API
    balance = data.get('data', {}).get('balance', 0)
    return balance

# --- Função para atualizar contador StreamElements ---
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
        balance = get_livepix_balance()
        print(f"Saldo LivePix: {balance}")

        result = update_streamelements_counter(balance)
        print("Contador StreamElements atualizado:", result)

    except Exception as e:
        print("Erro durante a sincronização:", e)

if __name__ == "__main__":
    main()
