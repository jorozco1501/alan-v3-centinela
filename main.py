from flask import Flask, request
import requests
import threading
import time
import datetime
import yfinance as yf
from option_chain import analizar_option_chain

# --- CONFIGURACIÓN ---
TOKEN = '7729218005:AAGAEyLMvvijyhRd5QpD33U9CiYQalkxflg'
API_URL = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
CHAT_ID = '7282485959'

# --- BOT TELEGRAM ---
app = Flask(__name__)

def enviar_mensaje(chat_id, texto):
    payload = {'chat_id': chat_id, 'text': texto}
    requests.post(API_URL, json=payload)

@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    if 'message' in data:
        chat_id = data['message']['chat']['id']
        texto = data['message'].get('text', '')

        if texto == '/start':
            respuesta = "Bienvenido al Alan Bot V3. Listo para ejecutar."
        elif texto == '/negro':
            respuesta = "Código NEGRO activado. Precisión táctica."
        elif texto == '/fantasma':
            respuesta = "Código Fantasma activado. Zona oscura en vigilancia."
        elif texto == '/titan':
            respuesta = "Código TITÁN activado. Swing Mode listo."
        elif texto == '/vaca':
            respuesta = "Código Vaca Entera activo. Vamos por todo."
        else:
            respuesta = "Comando no reconocido."

        enviar_mensaje(chat_id, respuesta)
    return 'OK'

# --- ESCANEO AUTOMÁTICO ---
def escaneo_periodico():
    while True:
        ahora = datetime.datetime.now()
        if ahora.weekday() < 5 and 7 <= ahora.hour < 14:
            mensaje_call = analizar_option_chain("QQQ", tipo="call")
            mensaje_put = analizar_option_chain("QQQ", tipo="put")
            enviar_mensaje(CHAT_ID, f"--- ESCANEO AUTOMÁTICO ---\n{mensaje_call}\n\n{mensaje_put}")
        time.sleep(300)  # Cada 5 minutos

# --- EJECUCIÓN 24/7 ---
if __name__ == '__main__':
    threading.Thread(target=escaneo_periodico).start()
    app.run(host='0.0.0.0', port=3000)
