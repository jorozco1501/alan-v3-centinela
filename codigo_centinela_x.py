from utils.telegram_alerta import enviar_alerta

def ejecutar_codigo_centinela_x(cadena_opciones):
    """
    Escanea la cadena de opciones buscando anomalías de volumen en contratos baratos.
    """
    for contrato in cadena_opciones:
        strike = contrato.get("strike")
        tipo = contrato.get("tipo")  # CALL o PUT
        precio = contrato.get("lastPrice", 0)
        volumen = contrato.get("volume", 0)
        oi = contrato.get("openInterest", 0)
        delta = contrato.get("delta", 0)

        if precio <= 1.00 and volumen > 1000:
            # Condición clave: volumen repentino y anormal
            if volumen > oi * 1.5 or (delta < 0.25 and volumen > 3000):
                mensaje = f"""Código CENTINELA X ACTIVADO
Anomalía detectada en contrato {tipo} {strike}
Precio: ${precio}
Volumen: {volumen} | Open Interest: {oi}
Delta: {delta}

Posible barrida institucional o carga silenciosa.
"""
                enviar_alerta(mensaje)
                return True
    return False
