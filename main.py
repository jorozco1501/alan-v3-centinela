from flask import Flask
import threading
from scheduler import iniciar_scheduler
from tendencia import obtener_tendencia
from entrada_ideal import detectar_entrada
from option_chain import obtener_mejor_contrato
from codigo_negro import ejecutar_codigo_negro
from codigos.codigo_fenix import ejecutar_codigo_fenix
from codigos.codigo_vaca import ejecutar_codigo_vaca
from grieta_latencia import detectar_grieta
from utils.telegram_alerta import enviar_alerta
from utils.logica_riesgo import calcular_riesgo

app = Flask(__name__)
@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    print("Mensaje recibido:", data)
    return 'OK', 200
# --- CONFIGURACIÓN ---
TICKER = "QQQ"
MAX_PRECIO_ENTRADA = 3.00
ultima_entrada = None

def escanear_y_ejecutar():
    global ultima_entrada

    tendencia = obtener_tendencia(TICKER)
    patron, estructura = detectar_entrada(TICKER)
    contrato = obtener_mejor_contrato(TICKER)

    if not contrato:
        print("Alan: No hay contrato disponible.")
        return

    precio_entrada = contrato['lastPrice']
    if precio_entrada > MAX_PRECIO_ENTRADA:
        print("Alan: Contrato fuera de rango ($).")
        return

    datos = {
        "tendencia": tendencia,
        "patron_velas": patron,
        "estructura": estructura
    }

    # 1. Grieta Fantasma (alta prioridad)
    if detectar_grieta(TICKER, contrato):
        return

    # 2. Sistema Modular de Códigos
    codigo_activado = None
    señal = None

    señal = ejecutar_codigo_negro(datos, contrato)
    if señal:
        codigo_activado = "Código NEGRO"
    else:
        señal = ejecutar_codigo_fenix(datos, contrato)
        if señal:
            codigo_activado = "Código FÉNIX"
        else:
            señal = ejecutar_codigo_vaca(datos, contrato)
            if señal:
                codigo_activado = "Código VACA ENTERA"

    # 3. Enviar alerta si hay código válido
    if señal:
        stop, target = calcular_riesgo(precio_entrada, señal["tipo"])
        ganancia = ((target - precio_entrada) / precio_entrada) * 100

        mensaje = f"""{codigo_activado} ACTIVADO en {TICKER}
Tendencia: {tendencia.upper()}
Entrada tipo: {señal['tipo']}
Precio entrada: ${precio_entrada:.2f}
STOP: ${stop:.2f}
TARGET: ${target:.2f}
Ganancia esperada: {ganancia:.1f}%
"""

        if mensaje != ultima_entrada:
            enviar_alerta(mensaje)
            ultima_entrada = mensaje
        else:
            print("Alan: Señal repetida. No se reenvía.")
    else:
        print("Alan: Sin señal táctica válida.")

if __name__ == "__main__":
    threading.Thread(target=iniciar_scheduler, args=(escanear_y_ejecutar,)).start()
    app.run(host="0.0.0.0", port=3000)
