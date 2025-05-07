from flask import Flask, request
import requests
import threading
import time
import datetime
import yfinance as yf

# --- CONFIGURACIÓN ---
TOKEN = '7729218005:AAGAEyLMvvijyhRd5QpD33U9CiYQalkxflg'
API_URL = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
CHAT_ID = '7282485959'  # Tu chat ID

# --- BOT TELEGRAM ---
app = Flask(__name__)

def analizar_qqq():
    ticker = yf.Ticker("QQQ")
    df = ticker.history(period="1d", interval="5m")

    if df.empty or len(df) < 3:
        return

    close = df['Close']
    high = df['High']
    low = df['Low']

    ultima = close[-1]
    anterior = close[-2]

    diferencia = abs(ultima - anterior)

    if diferencia < 0.60:
        # Movimiento débil, sin señal clara
        return

    if ultima > anterior:
        mensaje = (
            "CÓDIGO NEGRO ACTIVADO\n"
            "QQQ rompe con fuerza al alza.\n"
            f"Último precio: ${ultima:.2f}\n"
            f"Velas 5M confirman tendencia.\n"
            "Revisar CALL strike cercano para entrada táctica."
        )
    elif ultima < anterior:
        mensaje = (
            "CÓDIGO NEGRO ACTIVADO\n"
            "QQQ rompe con fuerza a la baja.\n"
            f"Último precio: ${ultima:.2f}\n"
            f"Velas 5M confirman impulso bajista.\n"
            "Revisar PUT strike cercano para entrada táctica."
        )
    else:
        return  # No hay movimiento claro

    enviar_mensaje(CHAT_ID, mensaje) 
