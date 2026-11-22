# registro_logs.py
# Configuracion del archivo de logs (logs/software_fj.log)

import logging
import os

# ruta del archivo, queda dentro de la carpeta logs del proyecto
RUTA_LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs", "software_fj.log")


def configurar_logger():
    os.makedirs(os.path.dirname(RUTA_LOG), exist_ok=True)  # crea la carpeta logs si no existe
    logger = logging.getLogger("SoftwareFJ")
    if not logger.handlers:  # para no agregar el handler dos veces
        logger.setLevel(logging.DEBUG)  # que guarde todo
        manejador = logging.FileHandler(RUTA_LOG, encoding="utf-8")  # utf-8 para las tildes
        formato = logging.Formatter("%(asctime)s | %(levelname)-8s | %(message)s",
                                    datefmt="%Y-%m-%d %H:%M:%S")  # fecha | nivel | mensaje
        manejador.setFormatter(formato)
        logger.addHandler(manejador)
    return logger


logger = configurar_logger()  # este es el que importan los otros archivos
