from utils.telegram_alerta import enviar_alerta
from utils.logica_riesgo import calcular_riesgo

def ejecutar_codigo_negro(ticker_data, contrato):
    tendencia = ticker_data.get("tendencia")
    patron = ticker_data.get("patron_velas")
    estructura = ticker_data.get("estructura")

    if tendencia == "alcista" and patron == "envolvente_alcista" and estructura == "rompimiento":
        mensaje = f"Código NEGRO activado para CALL.\nStrike: {contrato['strike']}\nDelta: {contrato['delta']}\nPrecio: ${contrato['lastPrice']}"
        enviar_alerta(mensaje)

        # Calcular salida
        targets = calcular_riesgo(contrato['lastPrice'])
        return {
            "tipo": "CALL",
            "entrada": contrato['lastPrice'],
            "target": targets["target"],
            "stop": targets["stop"]
        }
    
    elif tendencia == "bajista" and patron == "envolvente_bajista" and estructura == "rompimiento":
        mensaje = f"Código NEGRO activado para PUT.\nStrike: {contrato['strike']}\nDelta: {contrato['delta']}\nPrecio: ${contrato['lastPrice']}"
        enviar_alerta(mensaje)

        # Calcular salida
        targets = calcular_riesgo(contrato['lastPrice'])
        return {
            "tipo": "PUT",
            "entrada": contrato['lastPrice'],
            "target": targets["target"],
            "stop": targets["stop"]
        }
    
    return None
