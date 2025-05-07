import yfinance as yf

def analizar_option_chain(ticker_str, tipo='call'):
    ticker = yf.Ticker(ticker_str)
    expiraciones = ticker.options

    if not expiraciones:
        return "Sin expiraciones disponibles."

    expiracion = expiraciones[0]  # La más cercana
    cadena = ticker.option_chain(expiracion)

    opciones = cadena.calls if tipo == 'call' else cadena.puts

    mejores = opciones[
        (opciones['volume'] > 100) & 
        (opciones['impliedVolatility'] < 0.6) &
        (opciones['strike'] > ticker.history(period="1d")['Close'].iloc[-1] if tipo == 'call'
         else opciones['strike'] < ticker.history(period="1d")['Close'].iloc[-1])
    ]

    if mejores.empty:
        return f"No se detectaron {tipo.upper()}s buenos para hoy."

    mejor = mejores.sort_values(by='volume', ascending=False).iloc[0]
    mensaje = f"""
Se detectó un posible {tipo.upper()}:

Ticker: {ticker_str}
Strike: {mejor['strike']}
Expira: {expiracion}
Último precio del contrato: ${mejor['lastPrice']:.2f}
Volumen: {mejor['volume']}
IV: {mejor['impliedVolatility']:.2f}
"""

    return mensaje.strip()
