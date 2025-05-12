import schedule
import time
import threading
from utils.telegram_alerta import enviar_alerta  # Asegúrate que la ruta sea correcta

def tarea_programada():
    mensaje = "Tarea automática ejecutada por Alan Bot"
    print(mensaje)
    enviar_alerta(mensaje)

def iniciar_scheduler():
    schedule.every(10).seconds.do(tarea_programada)  # Puedes cambiar a .minutes si prefieres

    def run_scheduler():
        while True:
            schedule.run_pending()
            time.sleep(1)

    t = threading.Thread(target=run_scheduler)
    t.start()
