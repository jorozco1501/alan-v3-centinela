tipo = "CALL"  # o "PUT" si el movimiento fue bajista
strike = contrato['strike']
entrada = contrato['lastPrice']
stop, target = calcular_riesgo(entrada, tipo)

mensaje = f"""
Código GRIETA INVISIBLE detectado.
Tipo: {tipo}
Strike: {strike}
Entrada: ${entrada}
STOP táctico: ${stop}
TARGET proyectado: ${target}
"""
enviar_alerta(mensaje)
