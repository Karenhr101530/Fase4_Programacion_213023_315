import logging

# ==========================================
# 1. CONFIGURACIÓN DEL SISTEMA DE LOGS
# ==========================================
logging.basicConfig(
    filename='sistema_errores.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
    encoding='utf-8'
)

# ==========================================
# 2. EXCEPCIONES PERSONALIZADAS DE RESERVA
# ==========================================
class ReservaError(Exception):
    """Excepción base para errores relacionados con las reservas."""
    pass

class ReservaFallidaError(ReservaError):
    """Se lanza cuando ocurre un fallo al procesar, calcular o confirmar una reserva."""
    pass


# ==========================================
# 3. CLASE PRINCIPAL: RESERVA
# ==========================================
class Reserva:
    """
    Integra cliente, servicio, duración y estado, 
    implementando procesamiento con manejo avanzado de excepciones.
    """
    def __init__(self, id_reserva: str, cliente, servicio):
        self._id_reserva = id_reserva
        self._cliente = cliente
        self._servicio = servicio
        self._estado = "PENDIENTE"
        self._costo_total = 0.0

    @property
    def id_reserva(self) -> str:
        return self._id_reserva

    @property
    def estado(self) -> str:
        return self._estado

    @property
    def costo_total(self) -> float:
        return self._costo_total

    def procesar_reserva(self, *args, **kwargs):
        """
        Ejecuta la reserva aplicando la estructura robusta de excepciones:
        try / except / else / finally.
        """
        print(f"\n[Procesamiento] Iniciando transacción para Reserva ID: {self._id_reserva}")
        logging.info(f"Iniciando procesamiento de reserva {self._id_reserva} para el cliente {self._cliente.nombre}.")
        
        try:
            # Llamada al cálculo polimórfico del servicio asociado
            self._costo_total = self._servicio.calcular_costo(*args, **kwargs)
            self._estado = "CONFIRMADA"
            
        except (ValueError, TypeError, ReservaFallidaError) as ex:
            # Captura de errores operativos y de parámetros
            self._estado = "FALLIDA"
            error_msg = f"Error operativo en la reserva {self._id_reserva}: {ex}"
            logging.error(error_msg)
            print(f"[ERROR CAPTURADO] {error_msg}")
            
        except Exception as ex:
            # Captura de seguridad para cualquier error inesperado
            self._estado = "CANCELADA"
            error_msg = f"Error crítico inesperado en la reserva {self._id_reserva}: {ex}"
            logging.critical(error_msg)
            print(f"[ERROR CRÍTICO] {error_msg}")
            
        else:
            # Se ejecuta únicamente si la reserva fue exitosa sin excepciones
            success_msg = f"Reserva {self._id_reserva} confirmada con éxito. Total a pagar: ${self._costo_total:,.2f}"
            logging.info(success_msg)
            print(f"[ÉXITO] {success_msg}")
            
        finally:
            # Se ejecuta siempre (haya error o éxito), garantizando estabilidad del sistema
            print(f"[FINALLY] Estado final de la transacción [{self._id_reserva}]: {self._estado}")
            logging.info(f"Transacción {self._id_reserva} finalizada con estado de cierre: {self._estado}.")

    def cancelar_reserva(self):
        """Permite cancelar una reserva activa de forma controlada."""
        try:
            if self._estado == "CANCELADA":
                raise ReservaError("La reserva ya se encuentra cancelada.")
            
            self._estado = "CANCELADA"
            info_msg = f"La reserva {self._id_reserva} ha sido cancelada correctamente."
            logging.warning(info_msg)
            print(f"[CANCELACIÓN] {info_msg}")
            
        except ReservaError as e:
            logging.error(f"Fallo al intentar cancelar la reserva {self._id_reserva}: {e}")
            print(f"[ERROR] No se pudo cancelar: {e}")

    def obtener_detalles_reserva(self) -> str:
        """Retorna un resumen formateado de la reserva."""
        return (f"Reserva ID: {self._id_reserva} | "
                f"Cliente: {self._cliente.nombre} | "
                f"Servicio: {self._servicio._nombre_servicio} | "
                f"Estado: {self._estado} | "
                f"Total: ${self._costo_total:,.2f}")