from abc import ABC, abstractmethod
import math


# Excepcion general para los errores relacionados con los servicios.
class ServicioError(ValueError):
    pass


# Excepcion utilizada cuando un servicio no puede ofrecerse.
class ServicioNoDisponibleError(ServicioError):
    pass


# Clase abstracta que define las caracteristicas comunes de los servicios.
class Servicio(ABC):

    def __init__(self, nombre_servicio, tarifa_base, disponible=True):
        # Comprueba que el nombre del servicio sea un texto valido.
        if not isinstance(nombre_servicio, str) or not nombre_servicio.strip():
            raise ServicioError("El nombre del servicio no es valido.")

        # Guarda los datos del servicio y valida su tarifa.
        self._nombre_servicio = nombre_servicio.strip()
        self._tarifa_base = self.validar_numero(tarifa_base, "La tarifa")
        self._disponible = disponible

    # Permite consultar el nombre del servicio mediante una propiedad.
    @property
    def nombre_servicio(self):
        return self._nombre_servicio

    @staticmethod
    def validar_numero(valor, nombre):
        # Rechaza valores que no sean numericos, incluidos los booleanos.
        if isinstance(valor, bool) or not isinstance(valor, (int, float)):
            raise ServicioError(f"{nombre} debe ser numerico.")

        # Comprueba que el numero sea finito y mayor que cero.
        if not math.isfinite(valor) or valor <= 0:
            raise ServicioError(f"{nombre} debe ser mayor que cero.")

        return float(valor)

    def validar_disponibilidad(self):
        # Impide calcular costos de servicios que no estan disponibles.
        if not self._disponible:
            raise ServicioNoDisponibleError(
                f"El servicio {self._nombre_servicio} no esta disponible."
            )

    def calcular_precio(self, subtotal, descuento=0, impuesto=0.19):
        # Verifica que el descuento y el impuesto sean valores numericos.
        if isinstance(descuento, bool) or not isinstance(descuento, (int, float)):
            raise ServicioError("El descuento debe ser numerico.")

        if isinstance(impuesto, bool) or not isinstance(impuesto, (int, float)):
            raise ServicioError("El impuesto debe ser numerico.")

        # Valida que el descuento este entre 0 y 100 por ciento.
        if not math.isfinite(descuento) or not 0 <= descuento <= 100:
            raise ServicioError("El descuento debe estar entre 0 y 100.")

        # Valida que el impuesto sea una proporcion entre 0 y 1.
        if not math.isfinite(impuesto) or not 0 <= impuesto <= 1:
            raise ServicioError("El impuesto debe estar entre 0 y 1.")

        # Calcula el descuento y lo resta del subtotal.
        valor_descuento = subtotal * (descuento / 100)
        subtotal_con_descuento = subtotal - valor_descuento

        # Aplica el impuesto al valor que queda despues del descuento.
        return subtotal_con_descuento * (1 + impuesto)

    # Metodo abstracto que cada tipo de servicio debe implementar.
    @abstractmethod
    def calcular_costo(self, *args, **kwargs):
        pass

    # Obliga a las clases hijas a proporcionar su propia descripcion.
    @abstractmethod
    def describir_servicio(self):
        pass


# Clase hija que representa el servicio de reserva de salas.
class ReservaSala(Servicio):

    def __init__(self, tarifa_hora, capacidad_maxima=20, disponible=True):
        # Utiliza el constructor de Servicio para guardar los datos comunes.
        super().__init__("Reserva de salas", tarifa_hora, disponible)

        # Comprueba que la capacidad sea un numero entero positivo.
        if not isinstance(capacidad_maxima, int) or isinstance(capacidad_maxima, bool) or capacidad_maxima <= 0:
            raise ServicioError("La capacidad debe ser un entero positivo.")

        self._capacidad_maxima = capacidad_maxima

    def calcular_costo(self, horas, personas=1, descuento=0, impuesto=0.19):
        # Verifica que la sala este disponible y las horas sean validas.
        self.validar_disponibilidad()
        horas = self.validar_numero(horas, "Las horas")

        # Comprueba que la cantidad de personas sea un entero positivo.
        if not isinstance(personas, int) or isinstance(personas, bool) or personas <= 0:
            raise ServicioError("La cantidad de personas debe ser un entero positivo.")

        # Evita reservar una sala para mas personas de las permitidas.
        if personas > self._capacidad_maxima:
            raise ServicioError("Se supera la capacidad maxima de la sala.")

        # Calcula el costo segun las horas y aplica descuento e impuesto.
        return self.calcular_precio(horas * self._tarifa_base, descuento, impuesto)

    def describir_servicio(self):
        # Muestra la tarifa por hora y la capacidad maxima de la sala.
        return (f"{self._nombre_servicio}: Tarifa por hora ${self._tarifa_base:,.2f}. "
                f"Capacidad maxima: {self._capacidad_maxima} personas.")


# Clase hija que representa el alquiler de equipos.
class AlquilerEquipo(Servicio):

    def __init__(self, tarifa_hora, inventario=10, disponible=True):
        # Hereda la inicializacion de los datos generales del servicio.
        super().__init__("Alquiler de equipos", tarifa_hora, disponible)

        # Verifica que el inventario sea un entero mayor que cero.
        if not isinstance(inventario, int) or isinstance(inventario, bool) or inventario <= 0:
            raise ServicioError("El inventario debe ser un entero positivo.")

        self._inventario = inventario

    def calcular_costo(self, horas, cantidad=1, descuento=0, impuesto=0.19):
        # Comprueba la disponibilidad del servicio y valida las horas.
        self.validar_disponibilidad()
        horas = self.validar_numero(horas, "Las horas")

        # Verifica que la cantidad solicitada sea un entero positivo.
        if not isinstance(cantidad, int) or isinstance(cantidad, bool) or cantidad <= 0:
            raise ServicioError("La cantidad de equipos debe ser un entero positivo.")

        # Impide alquilar mas equipos de los que hay en inventario.
        if cantidad > self._inventario:
            raise ServicioNoDisponibleError("No hay suficientes equipos disponibles.")

        # Multiplica las horas por la tarifa y la cantidad de equipos.
        # Despues aplica el descuento y el impuesto correspondientes.
        return self.calcular_precio(horas * self._tarifa_base * cantidad, descuento, impuesto)

    def describir_servicio(self):
        # Devuelve la tarifa por equipo y el inventario disponible.
        return (f"{self._nombre_servicio}: Tarifa por hora y equipo ${self._tarifa_base:,.2f}. "
                f"Inventario disponible: {self._inventario}.")


# Clase hija que representa el servicio de asesoria especializada.
class AsesoriaEspecializada(Servicio):

    def __init__(self, tarifa_hora, disponible=True):
        # Inicializa el servicio utilizando el constructor de la clase padre.
        super().__init__("Asesoria especializada", tarifa_hora, disponible)

    def calcular_costo(self, horas, modalidad="virtual", descuento=0, impuesto=0.19):
        # Comprueba que el servicio este disponible y las horas sean validas.
        self.validar_disponibilidad()
        horas = self.validar_numero(horas, "Las horas")

        # Verifica que la modalidad ingresada sea un texto.
        if not isinstance(modalidad, str):
            raise ServicioError("La modalidad debe ser un texto.")

        # Elimina espacios y convierte la modalidad a minusculas.
        modalidad = modalidad.strip().lower()

        # Solo permite asesorias virtuales o presenciales.
        if modalidad not in ("virtual", "presencial"):
            raise ServicioError("La modalidad debe ser virtual o presencial.")

        # Calcula el costo inicial multiplicando las horas por la tarifa.
        subtotal = horas * self._tarifa_base

        # Aplica un recargo del 15 por ciento si la asesoria es presencial.
        if modalidad == "presencial":
            subtotal *= 1.15

        # Aplica el descuento y el impuesto al subtotal calculado.
        return self.calcular_precio(subtotal, descuento, impuesto)

    def describir_servicio(self):
        # Muestra la tarifa por hora y las modalidades disponibles.
        return (f"{self._nombre_servicio}: Tarifa por hora ${self._tarifa_base:,.2f}. "
                "Modalidades: virtual y presencial.")