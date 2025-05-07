def calcular_riesgo(precio_entrada, tipo="CALL"):
    stop = round(precio_entrada * 0.65, 2)  # Stop al -35%
    target = round(precio_entrada * 1.6, 2)  # Target al +60%
    return stop, target
