from flask import Flask, request
import requests

app = Flask(__name__)

TOKEN = 'TU_TOKEN_AQUI'
API_URL = f'https://api.telegram.org/bot{TOKEN}/sendMessage'

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
        else:
            respuesta = "Comando no reconocido."

        enviar_mensaje(chat_id, respuesta)
    return 'OK'

if __name__ == '__main__':
    import os
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 3000)))
