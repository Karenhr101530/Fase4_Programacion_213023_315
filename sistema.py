from cliente import GestionClientes
from services import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from reservas import Reserva, ReservaError
from registro import logger


# Clase principal que coordina la gestion de clientes, servicios y reservas.
class SistemaSoftwareFJ:

    def __init__(self):
        # Inicializa el gestor de clientes y las listas de servicios y reservas.
        self.clientes = GestionClientes()
        self.servicios = []
        self.reservas = []

    def registrar_cliente(self, nombre, documento, correo, telefono=None):
        # Registra un cliente utilizando las validaciones de GestionClientes.
        try:
            return self.clientes.registrar_cliente(
                nombre, documento, correo, telefono
            )

        except (ValueError, TypeError) as error:
            # Guarda el error en el archivo de logs y lo vuelve a generar.
            logger.error("Registro de cliente fallido: %s", error)
            raise

    def agregar_servicio(self, tipo, tarifa, **opciones):
        # Relaciona cada tipo de servicio con su clase correspondiente.
        clases = {
            "sala": ReservaSala,
            "equipo": AlquilerEquipo,
            "asesoria": AsesoriaEspecializada
        }

        try:
            # Comprueba que el tipo de servicio solicitado exista.
            if tipo not in clases:
                raise ValueError("Tipo de servicio no valido.")

            # Crea el objeto del servicio con su tarifa y opciones adicionales.
            servicio = clases[tipo](tarifa, **opciones)

        except (ValueError, TypeError) as error:
            # Registra el error y lo encadena a una nueva excepcion.
            logger.error("Creacion de servicio fallida: %s", error)
            raise RuntimeError("No se pudo crear el servicio.") from error

        else:
            # Guarda el servicio cuando su creacion fue exitosa.
            self.servicios.append(servicio)

            # Registra la creacion del servicio en el archivo de logs.
            logger.info("Servicio creado: %s", servicio.nombre_servicio)

            return servicio

    def crear_reserva(self, identificador, documento, servicio, duracion):
        # Crea una reserva relacionando un cliente con un servicio registrado.
        try:
            # Busca al cliente utilizando su numero de documento.
            cliente = self.clientes.buscar_cliente(documento)

            # Impide crear reservas para clientes que no estan registrados.
            if cliente is None:
                raise ReservaError("El cliente no esta registrado.")

            # Comprueba que el servicio pertenezca a los servicios registrados.
            if servicio not in self.servicios:
                raise ReservaError("El servicio no esta registrado.")

            # Evita que dos reservas tengan el mismo identificador.
            if any(r.id_reserva == identificador for r in self.reservas):
                raise ReservaError("El identificador de reserva ya existe.")

            # Crea el objeto Reserva con los datos validados.
            reserva = Reserva(identificador, cliente, servicio, duracion)

        except (ReservaError, ValueError, TypeError) as error:
            # Registra los errores y permite que sean controlados por el programa.
            logger.error("Creacion de reserva fallida: %s", error)
            raise

        else:
            # Guarda la reserva cuando todas las validaciones son correctas.
            self.reservas.append(reserva)

            # Registra la creacion de la reserva en el archivo de logs.
            logger.info("Reserva creada: %s", identificador)

            return reserva

    def buscar_reserva(self, identificador):
        # Recorre las reservas registradas para buscar su identificador.
        for reserva in self.reservas:

            # Devuelve la reserva cuando encuentra una coincidencia.
            if reserva.id_reserva == identificador:
                return reserva

        # Devuelve None cuando no existe una reserva con ese identificador.
        return None