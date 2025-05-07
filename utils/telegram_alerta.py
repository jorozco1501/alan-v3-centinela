import requests
import os

# Configuración
TOKEN = os.getenv("BOT_TOKEN", "7729218005:AAGAEyLMvvijyhRd5QpD33U9CiYQalkxflg")
CHAT_ID = os.getenv("CHAT_ID", "7282485959")
API_URL = f'https://api.telegram.org/bot{TOKEN}/sendMessage'

def enviar_alerta(mensaje):
    payload = {'chat_id': CHAT_ID, 'text': mensaje}
    requests.post(API_URL, json=payload)
