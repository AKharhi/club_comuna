import requests
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def obtener_coordenadas(direccion):
    response = requests.get(
        "https://maps.googleapis.com/maps/api/geocode/json",
        params={
            "address": direccion,
            "key": settings.GOOGLE_MAPS_API_KEY
        },
    )
    if response.status_code == 200:
        data = response.json()
        logger.info(f"Respuesta de la API: {data}")
        if data["results"]:
            location = data["results"][0]["geometry"]["location"]
            return location["lat"], location["lng"]
    else:
        logger.error(f"Error en la API: {response.status_code} - {response.text}")
    return None, None
