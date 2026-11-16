import unittest
from cliente import GestionClientes
from services import ReservaSala, AlquilerEquipo, AsesoriaEspecializada, ServicioError
from reservas import Reserva, ReservaError



# Clase que contiene las pruebas de integracion del sistema.
class PruebasIntegracion(unittest.TestCase):

    def setUp(self):
        # Prepara los datos antes de cada prueba.
        self.gestion = GestionClientes()
        self.cliente = self.gestion.registrar_cliente("Ana Gomez", "12345678", "ana@example.com")
        self.sala = ReservaSala(50000, capacidad_maxima=5)
        self.equipo = AlquilerEquipo(30000, inventario=3)
        self.asesoria = AsesoriaEspecializada(80000)

    def test_01_registro_cliente(self):
        # Busca al cliente que registramos.
        cliente_encontrado = self.gestion.buscar_cliente("12345678")

        if cliente_encontrado != self.cliente:
            self.fail("No se encontro el cliente registrado")

    def test_02_documento_duplicado(self):
        # Intenta registrar otro cliente con el mismo documento.
        try:
            self.gestion.registrar_cliente("Otro Cliente", "12345678", "otro@example.com")
        except ValueError:
            pass
        else:
            self.fail("El sistema permitio registrar un documento repetido")

    def test_03_correo_invalido(self):
        # Intenta registrar un correo que no es valido.
        try:
            self.gestion.registrar_cliente("Otro Cliente", "87654321", "correo_malo")
        except ValueError:
            pass
        else:
            self.fail("El sistema permitio registrar un correo incorrecto")

    def test_04_reserva_sala(self):
        # Crea y confirma una reserva de sala para 3 personas.
        reserva = Reserva("R01", self.cliente, self.sala, 2)

        if not reserva.confirmar_reserva(personas=3):
            self.fail("No se pudo confirmar la reserva de sala")

        if abs(reserva.costo_total - 119000) > 0.000001:
            self.fail("El costo de la sala es incorrecto")

    def test_05_descuento_sala(self):
        # Crea una reserva con descuento del 10 por ciento.
        reserva = Reserva("R02", self.cliente, self.sala, 2)

        if not reserva.confirmar_reserva(descuento=10):
            self.fail("No se pudo confirmar la reserva con descuento")

        if abs(reserva.costo_total - 107100) > 0.000001:
            self.fail("El descuento no se calculo correctamente")

    def test_06_equipo(self):
        # Alquila 2 equipos durante 2 horas.
        reserva = Reserva("R03", self.cliente, self.equipo, 2)

        if not reserva.confirmar_reserva(cantidad=2):
            self.fail("No se pudo confirmar el alquiler de equipos")

        if abs(reserva.costo_total - 142800) > 0.000001:
            self.fail("El costo del alquiler es incorrecto")

    def test_07_asesoria_presencial(self):
        # Reserva una asesoria presencial durante 2 horas.
        reserva = Reserva("R04", self.cliente, self.asesoria, 2)

        if not reserva.confirmar_reserva(modalidad="presencial"):
            self.fail("No se pudo confirmar la asesoria")

        if abs(reserva.costo_total - 218960) > 0.000001:
            self.fail("El costo de la asesoria es incorrecto")

    def test_08_capacidad_excedida(self):
        # La sala permite 5 personas, pero intentamos reservar para 6.
        reserva = Reserva("R05", self.cliente, self.sala, 1)

        if reserva.confirmar_reserva(personas=6):
            self.fail("Se permitio una reserva que supera la capacidad")

        if reserva.estado != "FALLIDA":
            self.fail("La reserva deberia estar en estado FALLIDA")

    def test_09_inventario_insuficiente(self):
        # Tenemos 3 equipos, pero intentamos reservar 4.
        reserva = Reserva("R06", self.cliente, self.equipo, 1)

        if reserva.confirmar_reserva(cantidad=4):
            self.fail("Se permitio reservar mas equipos de los disponibles")

    def test_10_horas_negativas(self):
        # Intenta crear una reserva con una duracion negativa.
        try:
            Reserva("R07", self.cliente, self.sala, -1)
        except ReservaError:
            pass
        else:
            self.fail("Se permitio crear una reserva con horas negativas")

    def test_11_cancelar_y_reprocesar(self):
        # Cancela una reserva e intenta confirmarla despues.
        reserva = Reserva("R08", self.cliente, self.sala, 2)

        if not reserva.cancelar_reserva():
            self.fail("No se pudo cancelar la reserva")

        if reserva.confirmar_reserva():
            self.fail("Se permitio confirmar una reserva cancelada")

        if reserva.estado != "CANCELADA":
            self.fail("La reserva deberia continuar CANCELADA")

    def test_12_no_confirmar_dos_veces(self):
        # Confirma una reserva e intenta procesarla nuevamente.
        reserva = Reserva("R09", self.cliente, self.sala, 2)

        if not reserva.confirmar_reserva():
            self.fail("No se pudo confirmar la reserva")

        if reserva.procesar_reserva():
            self.fail("Se permitio procesar dos veces la misma reserva")

        if reserva.estado != "CONFIRMADA":
            self.fail("La reserva deberia continuar CONFIRMADA")

    def test_13_servicio_no_disponible(self):
        # Intenta reservar una sala que no esta disponible.
        reserva = Reserva("R10", self.cliente, ReservaSala(50000, disponible=False), 1)

        if reserva.confirmar_reserva():
            self.fail("Se permitio reservar un servicio no disponible")

    def test_14_descuento_invalido(self):
        # Intenta aplicar un descuento mayor al 100 por ciento.
        reserva = Reserva("R11", self.cliente, self.sala, 1)

        if reserva.confirmar_reserva(descuento=120):
            self.fail("Se permitio aplicar un descuento invalido")

    def test_15_modalidad_invalida(self):
        # Intenta solicitar una asesoria con una modalidad no permitida.
        reserva = Reserva("R12", self.cliente, self.asesoria, 1)

        if reserva.confirmar_reserva(modalidad="telefono"):
            self.fail("Se permitio una modalidad de asesoria incorrecta")

    def test_16_cliente_invalido(self):
        # Intenta crear una reserva utilizando un texto en lugar de un cliente.
        try:
            Reserva("R13", "Ana", self.sala, 2)
        except ReservaError:
            pass
        else:
            self.fail("Se permitio crear una reserva sin un cliente valido")

    def test_17_duracion_no_duplicada(self):
        # Intenta cambiar las horas al momento de confirmar.
        reserva = Reserva("R14", self.cliente, self.sala, 2)

        if reserva.confirmar_reserva(horas=5):
            self.fail("Se permitio indicar nuevamente las horas de reserva")

    def test_18_costo_nan(self):
        # Intenta calcular un costo con un descuento numerico invalido.
        try:
            self.sala.calcular_costo(2, descuento=float("nan"))
        except ServicioError:
            pass
        else:
            self.fail("Se permitio calcular un costo con un valor invalido")


# Ejecuta las pruebas cuando se abre este archivo directamente.
if __name__ == "__main__":
    unittest.main(verbosity=2)
