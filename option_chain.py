import yfinance as yf

def obtener_mejor_contrato(ticker_simbolo):
    ticker = yf.Ticker(ticker_simbolo)
    expiraciones = ticker.options

    if not expiraciones:
        return None

    # Tomamos la expiración más cercana (ideal para intradía)
    expiracion = expiraciones[0]
    cadena = ticker.option_chain(expiracion)

    contratos_call = cadena.calls
    contratos_filtrados = []

    for _, row in contratos_call.iterrows():
        contrato = {
            "strike": row["strike"],
            "tipo": "CALL",
            "lastPrice": row["lastPrice"],
            "volume": row["volume"],
            "openInterest": row["openInterest"],
            "impliedVolatility": row["impliedVolatility"],
            "delta": row.get("delta", 0) or 0  # algunas versiones no traen delta
        }

        if 0.10 <= contrato["lastPrice"] <= 3.00:
            contratos_filtrados.append(contrato)

    # Seleccionamos uno con delta medio
    contrato_sugerido = next((c for c in contratos_filtrados if 0.38 <= c["delta"] <= 0.55), None)

    return {
        "strike": contrato_sugerido["strike"] if contrato_sugerido else None,
        "tipo": "CALL",
        "lastPrice": contrato_sugerido["lastPrice"] if contrato_sugerido else None,
        "delta": contrato_sugerido["delta"] if contrato_sugerido else None,
        "cadena_completa": contratos_filtrados
    }
