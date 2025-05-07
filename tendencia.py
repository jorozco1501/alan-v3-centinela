import yfinance as yf

def detectar_tendencia(ticker):
    simbolo = yf.Ticker(ticker)

    try:
        tf_5m = simbolo.history(period="1d", interval="5m")
        tf_15m = simbolo.history(period="1d", interval="15m")
        tf_1h = simbolo.history(period="5d", interval="60m")

        if tf_5m.empty or tf_15m.empty or tf_1h.empty:
            return None

        def es_alcista(df):
            return df['Close'].iloc[-1] > df['Close'].iloc[0]

        def es_bajista(df):
            return df['Close'].iloc[-1] < df['Close'].iloc[0]

        alcista_5m = es_alcista(tf_5m)
        alcista_15m = es_alcista(tf_15m)
        alcista_1h = es_alcista(tf_1h)

        bajista_5m = es_bajista(tf_5m)
        bajista_15m = es_bajista(tf_15m)
        bajista_1h = es_bajista(tf_1h)

        if alcista_5m and alcista_15m and alcista_1h:
            return "Tendencia alcista fuerte detectada en QQQ. Posible entrada CALL."

        elif bajista_5m and bajista_15m and bajista_1h:
            return "Tendencia bajista fuerte detectada en QQQ. Posible entrada PUT."

        else:
            return None

    except Exception as e:
        return None
