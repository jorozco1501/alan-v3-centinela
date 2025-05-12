import schedule
import time
import threading
from utils.telegram_alerta import enviar_alerta
from entrada_ideal import detectar_entrada_ideal

ultima_senal = None  # memoria táctica

def tarea_programada():
    global ultima_senal

    datos = detectar_entrada_ideal("QQQ")
    if datos:
        mensaje = f"""
Alan Bot – Señal automática

Tipo: {datos['tipo']}
Strike: {datos['strike']}
Entrada: ${datos['entrada']}
Target: ${datos['target']}
Stop: ${datos['stop']}
Delta: {datos['delta']:.2f}
""".strip()

        if mensaje != ultima_senal:
            enviar_alerta(mensaje)
            print("Señal enviada por Alan Bot:")
            print(mensaje)
            ultima_senal = mensaje
        else:
            print("Señal repetida. No se envía.")
    else:
        print("Sin señal válida en este ciclo.")

def iniciar_scheduler():
    schedule.every(5).minutes.do(tarea_programada)

    def run_scheduler():
        while True:
            schedule.run_pending()
            time.sleep(1)

    t = threading.Thread(target=run_scheduler)
    t.start()
