import yfinance as yf

def obtener_tendencia(ticker):
    marcos = {
        '1m': '1m',
        '5m': '5m',
        '15m': '15m',
        '1h': '60m',
        '1d': '1d'
    }

    resultados = {}

    for nombre, intervalo in marcos.items():
        try:
            datos = yf.Ticker(ticker).history(period='1d', interval=intervalo)
            if len(datos) < 2:
                resultados[nombre] = 'sin datos'
                continue

            close_actual = datos['Close'].iloc[-1]
            close_anterior = datos['Close'].iloc[-2]

            if close_actual > close_anterior:
                resultados[nombre] = 'alcista'
            elif close_actual < close_anterior:
                resultados[nombre] = 'bajista'
            else:
                resultados[nombre] = 'neutra'
        except Exception as e:
            resultados[nombre] = f'error: {e}'

    return resultados

# Prueba directa (solo para testeo)
if __name__ == "__main__":
    tendencia = obtener_tendencia("QQQ")
    for marco, direccion in tendencia.items():
        print(f"Tendencia en {marco}: {direccion}")
