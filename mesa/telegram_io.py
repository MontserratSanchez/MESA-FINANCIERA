"""Comunicación con Telegram mediante la Bot API (solo peticiones HTTP, sin librerías extra)."""
import requests

from . import config

LIMITE_MENSAJE = 4000          # Telegram acepta hasta 4096 caracteres por mensaje


def ocultar_llaves(texto):
    """Reemplaza cualquier llave configurada por *** (los errores de red incluyen la URL con el token)."""
    texto = str(texto)
    for llave in (config.TELEGRAM_BOT_TOKEN, config.ANTHROPIC_API_KEY, config.ALPHAVANTAGE_API_KEY):
        if llave:
            texto = texto.replace(llave, "***")
    return texto


def _url(metodo):
    if not config.TELEGRAM_BOT_TOKEN:
        raise RuntimeError("Falta TELEGRAM_BOT_TOKEN (créalo con @BotFather).")
    return f"https://api.telegram.org/bot{config.TELEGRAM_BOT_TOKEN}/{metodo}"


def _pedir(verbo, metodo, **opciones):
    """Hace la petición a Telegram; si falla la red, relanza el mismo tipo de error SIN el token."""
    try:
        return getattr(requests, verbo)(_url(metodo), **opciones).json()
    except requests.RequestException as error:
        raise type(error)(ocultar_llaves(error)) from None


def enviar(chat_id, texto):
    datos = _pedir("post", "sendMessage",
                   data={"chat_id": chat_id, "text": texto[:LIMITE_MENSAJE]}, timeout=20)
    if not datos.get("ok"):
        raise RuntimeError(f"Telegram rechazó el mensaje: {datos.get('description')}")
    return datos


def verificar_bot():
    """Devuelve el @usuario del bot o lanza un error claro si el token es inválido."""
    datos = _pedir("get", "getMe", timeout=20)
    if not datos.get("ok"):
        raise RuntimeError("Token de Telegram inválido. Revísalo con @BotFather.")
    return datos["result"]["username"]


def preparar_polling():
    """Quita un webhook previo; si existe, getUpdates no funciona."""
    _pedir("get", "deleteWebhook", timeout=20)


def obtener_mensajes(offset=None, espera=0):
    """Mensajes pendientes. Telegram los guarda hasta 24 h si nadie los lee."""
    parametros = {"timeout": espera}
    if offset is not None:
        parametros["offset"] = offset
    datos = _pedir("get", "getUpdates", params=parametros, timeout=espera + 15)
    if not datos.get("ok"):
        raise RuntimeError(f"getUpdates falló: {datos.get('description')}")
    return datos["result"]


def confirmar_leidos(ultimo_update_id):
    """Marca como leídos todos los mensajes hasta ese id, para no procesarlos dos veces."""
    obtener_mensajes(offset=ultimo_update_id + 1)


def chat_autorizado(chat_id):
    """Solo el chat de TELEGRAM_CHAT_ID puede usar el bot.

    Seguridad: en modo real, si TELEGRAM_CHAT_ID está vacío nadie queda autorizado
    (antes cualquier desconocido podía gastar tu cuota y tu saldo). En simulación no hay costo.
    """
    if not config.TELEGRAM_CHAT_ID:
        return config.MODO_SIMULACION
    return str(chat_id) == config.TELEGRAM_CHAT_ID
