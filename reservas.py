import logging
import math
from cliente import Cliente
from services import Servicio, ServicioError
from registro import logger


# Excepcion general para los errores relacionados con las reservas.
class ReservaError(Exception):
    pass


# Excepcion utilizada cuando una reserva no puede procesarse correctamente.
class ReservaFallidaError(ReservaError):
    pass


# Clase encargada de relacionar clientes, servicios y reservas.
class Reserva:

    def __init__(self, id_reserva, cliente, servicio, duracion):
        # Valida que el identificador de la reserva no este vacio.
        if not isinstance(id_reserva, str) or not id_reserva.strip():
            raise ReservaError("El identificador de la reserva no es valido.")

        # Comprueba que el cliente sea un objeto de la clase Cliente.
        if not isinstance(cliente, Cliente):
            raise ReservaError("La reserva necesita un cliente valido.")

        # Verifica que el servicio pertenezca a la clase Servicio.
        if not isinstance(servicio, Servicio):
            raise ReservaError("La reserva necesita un servicio valido.")

        # Comprueba que la duracion sea un numero positivo y valido.
        if isinstance(duracion, bool) or not isinstance(duracion, (int, float)) or not math.isfinite(duracion) or duracion <= 0:
            raise ReservaError("La duracion debe ser un numero mayor que cero.")

        # Guarda los datos de la reserva e inicia su estado como pendiente.
        self._id_reserva = id_reserva.strip()
        self._cliente = cliente
        self._servicio = servicio
        self._duracion = float(duracion)
        self._estado = "PENDIENTE"
        self._costo_total = 0.0

    # Propiedades que permiten consultar los datos de la reserva.
    @property
    def id_reserva(self):
        return self._id_reserva

    @property
    def estado(self):
        return self._estado

    @property
    def costo_total(self):
        return self._costo_total

    @property
    def duracion(self):
        return self._duracion

    # Procesa la reserva, calcula su costo y controla los posibles errores.
    def procesar_reserva(self, **kwargs):
        print(f"\n[Procesamiento] Reserva ID: {self._id_reserva}")

        # Registra el inicio del procesamiento en el archivo de logs.
        logger.info("Iniciando reserva %s para %s", self._id_reserva, self._cliente.nombre)

        exito = False

        try:
            # Impide procesar reservas que ya fueron confirmadas, canceladas o fallidas.
            if self._estado != "PENDIENTE":
                raise ReservaFallidaError("Solo se pueden procesar reservas pendientes.")

            # Evita ingresar nuevamente las horas porque ya estan guardadas.
            if "horas" in kwargs:
                raise ReservaFallidaError("Las horas ya estan definidas en la reserva.")

            # Calcula el costo utilizando el metodo del servicio seleccionado.
            self._costo_total = self._servicio.calcular_costo(
                horas=self._duracion, **kwargs
            )

            # Verifica que el costo calculado sea numerico y no sea negativo.
            costo = self._costo_total
            if isinstance(costo, bool) or not isinstance(costo, (int, float)) or not math.isfinite(costo) or costo < 0:
                raise ReservaFallidaError("El costo calculado no es valido.")

            # Actualiza el costo y confirma la reserva cuando todo es correcto.
            self._costo_total = float(costo)
            self._estado = "CONFIRMADA"
            exito = True

        except (ServicioError, ValueError, TypeError, ReservaError) as error:
            # Captura errores de validacion, calculos o condiciones del servicio.
            # Solo cambia a FALLIDA si la reserva estaba pendiente.
            if self._estado == "PENDIENTE":
                self._estado = "FALLIDA"

            # Registra el error y muestra un mensaje sin detener el programa.
            logger.error("Error en reserva %s: %s", self._id_reserva, error)
            print(f"[VALIDACION] Reserva rechazada: {error}")

        except Exception as error:
            # Controla errores inesperados para mantener estable el sistema.
            if self._estado == "PENDIENTE":
                self._estado = "FALLIDA"

            # Guarda los detalles del error inesperado en el archivo de logs.
            logger.exception("Error inesperado en reserva %s", self._id_reserva)
            print(f"[ERROR INESPERADO] {error}")

        else:
            # Se ejecuta solamente cuando la reserva se procesa sin errores.
            logger.info("Reserva %s confirmada. Total: %.2f", self._id_reserva, self._costo_total)
            print(f"[EXITO] Reserva confirmada. Total: ${self._costo_total:,.2f}")

        finally:
            # Se ejecuta siempre, sin importar si la reserva fue exitosa o fallida.
            print(f"[FINALLY] Estado final: {self._estado}")
            logger.info("Reserva %s finalizada: %s", self._id_reserva, self._estado)

        # Devuelve True si la reserva fue confirmada o False si hubo un error.
        return exito

    # Utiliza el procesamiento para confirmar una reserva.
    def confirmar_reserva(self, **kwargs):
        return self.procesar_reserva(**kwargs)

    # Permite cancelar una reserva y registra el resultado.
    def cancelar_reserva(self):

        # Evita cancelar nuevamente una reserva que ya fue cancelada.
        if self._estado == "CANCELADA":
            logger.warning("La reserva %s ya estaba cancelada", self._id_reserva)
            print("[ERROR] La reserva ya esta cancelada.")
            return False

        # Cambia el estado a cancelada y registra el evento.
        self._estado = "CANCELADA"
        logger.warning("Reserva %s cancelada", self._id_reserva)
        print(f"[CANCELACION] Reserva {self._id_reserva} cancelada.")

        return True

    # Reune la informacion principal de la reserva para mostrarla.
    def obtener_detalles_reserva(self):
        return (f"Reserva ID: {self._id_reserva} | "
                f"Cliente: {self._cliente.nombre} | "
                f"Servicio: {self._servicio.nombre_servicio} | "
                f"Duracion: {self._duracion:g} horas | "
                f"Estado: {self._estado} | "
                f"Total: ${self._costo_total:,.2f}")
        