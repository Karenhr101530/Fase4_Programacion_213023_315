import logging


def configurar_logs():
    # Configura el registro de eventos y errores del sistema.
    logger = logging.getLogger("software_fj")
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        archivo = logging.FileHandler("sistema_errores.log", encoding="utf-8")
        archivo.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
        logger.addHandler(archivo)
    return logger


logger = configurar_logs()
