
from abc import ABC, abstractmethod
import math


# ==========================================
# 1. EXCEPCIONES PERSONALIZADAS
# ==========================================

class ServicioError(ValueError):
    """Error relacionado con la gestión de servicios."""
    pass


class ServicioNoDisponibleError(ServicioError):
    """Se genera cuando un servicio no está disponible."""
    pass


# ==========================================
# 2. CLASE ABSTRACTA SERVICIO
# ==========================================

class Servicio(ABC):
    """Clase abstracta que representa un servicio general."""

    def __init__(self, nombre_servicio, tarifa_base, disponible=True):
        if not isinstance(nombre_servicio, str) or not nombre_servicio.strip():
            raise ServicioError("El nombre del servicio no es válido.")

        self._nombre_servicio = nombre_servicio.strip()
        self._tarifa_base = self.validar_numero(tarifa_base, "La tarifa")
        self._disponible = disponible

    @staticmethod
    def validar_numero(valor, nombre):
        if isinstance(valor, bool) or not isinstance(valor, (int, float)):
            raise ServicioError(f"{nombre} debe ser numérico.")

        if not math.isfinite(valor) or valor <= 0:
            raise ServicioError(f"{nombre} debe ser mayor que cero.")

        return float(valor)

    def validar_disponibilidad(self):
        if not self._disponible:
            raise ServicioNoDisponibleError(
                f"El servicio {self._nombre_servicio} no está disponible."
            )

    def calcular_precio(self, subtotal, descuento=0, impuesto=0.19):
        """Calcula el valor final aplicando descuento e impuesto."""

        if isinstance(descuento, bool) or not isinstance(descuento, (int, float)):
            raise ServicioError("El descuento debe ser numérico.")

        if isinstance(impuesto, bool) or not isinstance(impuesto, (int, float)):
            raise ServicioError("El impuesto debe ser numérico.")

        if not 0 <= descuento <= 100:
            raise ServicioError("El descuento debe estar entre 0 y 100.")

        if not 0 <= impuesto <= 1:
            raise ServicioError("El impuesto debe estar entre 0 y 1.")

        valor_descuento = subtotal * (descuento / 100)
        subtotal_con_descuento = subtotal - valor_descuento

        return subtotal_con_descuento * (1 + impuesto)

    @abstractmethod
    def calcular_costo(self, *args, **kwargs):
        """Cada servicio implementa su propio cálculo de costo."""
        pass

    @abstractmethod
    def describir_servicio(self):
        """Describe las características del servicio."""
        pass


# ==========================================
# 3. SERVICIO DE RESERVA DE SALAS
# ==========================================

class ReservaSala(Servicio):

    def __init__(self, tarifa_hora, capacidad_maxima=20, disponible=True):
        super().__init__("Reserva de salas", tarifa_hora, disponible)

        if not isinstance(capacidad_maxima, int) or isinstance(capacidad_maxima, bool) or capacidad_maxima <= 0:
            raise ServicioError("La capacidad debe ser un entero positivo.")

        self._capacidad_maxima = capacidad_maxima

    def calcular_costo(self, horas, personas=1, descuento=0, impuesto=0.19):
        self.validar_disponibilidad()

        horas = self.validar_numero(horas, "Las horas")

        if not isinstance(personas, int) or isinstance(personas, bool) or personas <= 0:
            raise ServicioError("La cantidad de personas debe ser un entero positivo.")

        if personas > self._capacidad_maxima:
            raise ServicioError("Se supera la capacidad máxima de la sala.")

        subtotal = horas * self._tarifa_base

        return self.calcular_precio(subtotal, descuento, impuesto)

    def describir_servicio(self):
        return (
            f"{self._nombre_servicio}: "
            f"Tarifa por hora ${self._tarifa_base:,.2f}. "
            f"Capacidad máxima: {self._capacidad_maxima} personas."
        )


# ==========================================
# 4. SERVICIO DE ALQUILER DE EQUIPOS
# ==========================================

class AlquilerEquipo(Servicio):

    def __init__(self, tarifa_hora, inventario=10, disponible=True):
        super().__init__("Alquiler de equipos", tarifa_hora, disponible)

        if not isinstance(inventario, int) or isinstance(inventario, bool) or inventario <= 0:
            raise ServicioError("El inventario debe ser un entero positivo.")

        self._inventario = inventario

    def calcular_costo(self, horas, cantidad=1, descuento=0, impuesto=0.19):
        self.validar_disponibilidad()

        horas = self.validar_numero(horas, "Las horas")

        if not isinstance(cantidad, int) or isinstance(cantidad, bool) or cantidad <= 0:
            raise ServicioError("La cantidad de equipos debe ser un entero positivo.")

        if cantidad > self._inventario:
            raise ServicioNoDisponibleError(
                "No hay suficientes equipos disponibles."
            )

        subtotal = horas * self._tarifa_base * cantidad

        return self.calcular_precio(subtotal, descuento, impuesto)

    def describir_servicio(self):
        return (
            f"{self._nombre_servicio}: "
            f"Tarifa por hora y equipo ${self._tarifa_base:,.2f}. "
            f"Inventario disponible: {self._inventario}."
        )


# ==========================================
# 5. SERVICIO DE ASESORÍAS ESPECIALIZADAS
# ==========================================

class AsesoriaEspecializada(Servicio):

    def __init__(self, tarifa_hora, disponible=True):
        super().__init__("Asesoría especializada", tarifa_hora, disponible)

    def calcular_costo(self, horas, modalidad="virtual",
                       descuento=0, impuesto=0.19):

        self.validar_disponibilidad()

        horas = self.validar_numero(horas, "Las horas")

        if not isinstance(modalidad, str):
            raise ServicioError("La modalidad debe ser un texto.")

        modalidad = modalidad.strip().lower()

        if modalidad not in ("virtual", "presencial"):
            raise ServicioError(
                "La modalidad debe ser virtual o presencial."
            )

        subtotal = horas * self._tarifa_base

        # Las asesorías presenciales tienen un recargo del 15%.
        if modalidad == "presencial":
            subtotal *= 1.15

        return self.calcular_precio(subtotal, descuento, impuesto)

    def describir_servicio(self):
        return (
            f"{self._nombre_servicio}: "
            f"Tarifa por hora ${self._tarifa_base:,.2f}. "
            f"Modalidades: virtual y presencial."
        )
