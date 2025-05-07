def calcular_zona_entrada(precio_actual):
    ideal = round(precio_actual * 0.95, 2)
    maximo = round(precio_actual * 1.10, 2)
    return ideal, maximo

def evaluar_entrada(contrato):
    strike = contrato.get("strike")
    delta = contrato.get("delta")
    volumen = contrato.get("volume")
    precio = contrato.get("lastPrice")

    if not all([strike, delta, volumen, precio]):
        return None

    ideal, maximo = calcular_zona_entrada(precio)

    mensaje = f"""Entrada táctica detectada:
Contrato: {strike}
Último precio: ${precio}
Delta: {delta}
Volumen: {volumen}
Zona ideal de entrada: ${ideal}
Evitar si pasa de: ${maximo}
"""

    return mensaje.strip()
