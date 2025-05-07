import yfinance as yf
from datetime import datetime

def escanear(ticker):
    datos = yf.Ticker(ticker).history(period="1d", interval="5m")
    if datos.empty:
        return None

    ultima = datos.iloc[-1]
    precio = ultima['Close']
    return f"{ticker} → Precio actual: {precio} - {datetime.now().strftime('%H:%M:%S')}"

# Ejemplo de prueba
if __name__ == "__main__":
    print(escanear("QQQ"))
    print(escanear("NVDA"))
