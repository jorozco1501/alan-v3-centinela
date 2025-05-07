from flask import Flask, request
import requests
import threading
import time
import datetime
import yfinance as yf

# --- CONFIGURACIÓN ---
TOKEN = '7729218005:AAGAEyLMvvijyhRd5QpD33U9CiYQalkxflg'
API_URL = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
CHAT_ID = '7282485959'  # Tu chat ID

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

# --- ESCANEO AUTOMÁTICO (cada 5 minutos) ---
def escaneo_periodico():
    while True:
        ahora = datetime.datetime.now()
        if ahora.weekday() < 5 and 7 <= ahora.hour < 14:
            analizar_qqq()
        time.sleep(300)  # 5 minutos

def analizar_qqq():
    ticker = yf.Ticker("QQQ")
    df = ticker.history(period="1d", interval="5m")
    if df.empty:
        return

    close = df['Close']
    if close[-1] > close[-2]:
        mensaje = "QQQ subiendo: posible oportunidad CALL.\nÚltimo precio: ${:.2f}".format(close[-1])
    else:
        mensaje = "QQQ bajando: posible oportunidad PUT.\nÚltimo precio: ${:.2f}".format(close[-1])
    
    enviar_mensaje(CHAT_ID, mensaje)

# --- EJECUCIÓN 24/7 ---
if __name__ == '__main__':
    threading.Thread(target=escaneo_periodico).start()
    app.run(host='0.0.0.0', port=3000)
