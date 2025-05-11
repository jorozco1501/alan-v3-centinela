import schedule
import time
import threading

def tarea_programada():
    print("Tarea automática ejecutada por Alan Bot")

def iniciar_scheduler():
    schedule.every(10).seconds.do(tarea_programada)

    def run_scheduler():
        while True:
            schedule.run_pending()
            time.sleep(1)

    t = threading.Thread(target=run_scheduler)
    t.start()
