
import unittest
from entidad import Entidad
from cliente import Cliente
from sistema import SistemaSoftwareFJ


# Verifica que el sistema cumpla con los requisitos de la Fase 4.
class PruebasRequisitos(unittest.TestCase):

    def setUp(self):
        # Crea los objetos necesarios antes de cada prueba.
        self.sistema = SistemaSoftwareFJ()
        self.cliente = self.sistema.registrar_cliente(
            "Ana Gomez", "12345678", "ana@example.com"
        )
        self.sala = self.sistema.agregar_servicio("sala", 50000)

    def test_entidad_abstracta(self):
        # Comprueba que Cliente herede de la clase abstracta Entidad.
        if not isinstance(self.cliente, Entidad):
            self.fail("Cliente no hereda de la clase Entidad")

        # Comprueba que no se pueda crear un objeto de Entidad.
        try:
            Entidad()
        except TypeError:
            pass
        else:
            self.fail("Se permitio crear un objeto de la clase abstracta")

    def test_cliente_no_registrado(self):
        # Intenta crear una reserva para un cliente que no existe.
        try:
            self.sistema.crear_reserva(
                "R01", "99999999", self.sala, 2
            )
        except Exception:
            pass
        else:
            self.fail("Se permitio reservar con un cliente no registrado")

    def test_servicio_no_registrado(self):
        # Crea un servicio que no esta registrado en el sistema.
        from services import ReservaSala

        servicio_externo = ReservaSala(1000)

        # Intenta crear una reserva con ese servicio.
        try:
            self.sistema.crear_reserva(
                "R01", "12345678", servicio_externo, 2
            )
        except Exception:
            pass
        else:
            self.fail("Se permitio reservar un servicio no registrado")

    def test_identificador_duplicado(self):
        # Registra una reserva con el identificador R01.
        self.sistema.crear_reserva(
            "R01", "12345678", self.sala, 2
        )

        # Intenta registrar otra reserva con el mismo identificador.
        try:
            self.sistema.crear_reserva(
                "R01", "12345678", self.sala, 3
            )
        except Exception:
            pass
        else:
            self.fail("Se permitio registrar una reserva duplicada")

    def test_encadenamiento_excepciones(self):
        # Intenta crear un servicio con una tarifa negativa.
        try:
            self.sistema.agregar_servicio("sala", -5)

        except RuntimeError as error:
            # Comprueba que el error conserve su causa original.
            if error.__cause__ is None:
                self.fail("El error no conserva la excepcion original")

        else:
            self.fail("No se genero el error esperado")


# Permite ejecutar las pruebas directamente desde este archivo.
if __name__ == "__main__":
    unittest.main()
