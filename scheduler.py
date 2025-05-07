import schedule
import time
import requests

def ejecutar_centinela():
    url = "https://alan-v3-centinela.up.railway.app/scan"
    try:
        response = requests.get(url)
        print(f"Escaneo ejecutado - Respuesta: {response.status_code}")
    except Exception as e:
        print(f"Error al ejecutar el escaneo: {e}")

# Ejecutar cada 5 minutos
schedule.every(5).minutes.do(ejecutar_centinela)

while True:
    schedule.run_pending()
    time.sleep(1)
