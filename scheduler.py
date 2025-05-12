import schedule
import time
import threading
from utils.telegram_alerta import enviar_alerta
from entrada_ideal import detectar_entrada_ideal  # ajusta si está en otra carpeta

def tarea_programada():
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
"""
        enviar_alerta(mensaje)
        print(mensaje)
    else:
        print("Sin señal válida en este ciclo.")

def iniciar_scheduler():
    schedule.every(5).minutes.do(tarea_programada)  # cambio aquí

    def run_scheduler():
        while True:
            schedule.run_pending()
            time.sleep(1)

    t = threading.Thread(target=run_scheduler)
    t.start()i
