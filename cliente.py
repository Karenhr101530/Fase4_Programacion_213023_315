
import re


class Cliente:
    """Representa un cliente del sistema."""

    def __init__(self, nombre, documento, correo, telefono=None):
        self.__nombre = self.validar_nombre(nombre)
        self.__documento = self.validar_documento(documento)
        self.__correo = self.validar_correo(correo)
        self.__telefono = self.validar_telefono(telefono)

    # Validaciones de los datos
    @staticmethod
    def validar_nombre(nombre):
        if not isinstance(nombre, str) or not nombre.strip():
            raise ValueError("El nombre no puede estar vacio.")

        nombre = nombre.strip()

        if len(nombre) < 3:
            raise ValueError("El nombre debe tener al menos 3 caracteres.")

        if not all(letra.isalpha() or letra.isspace()
                   for letra in nombre):
            raise ValueError("El nombre solo debe contener letras.")

        return nombre

    @staticmethod
    def validar_documento(documento):
        if not isinstance(documento, str):
            raise ValueError("El documento debe ser un texto numerico.")

        documento = documento.strip()

        if not documento.isdigit() or not 6 <= len(documento) <= 12:
            raise ValueError(
                "El documento debe contener entre 6 y 12 numeros."
            )

        return documento

    @staticmethod
    def validar_correo(correo):
        if not isinstance(correo, str):
            raise ValueError("El correo debe ser un texto.")

        correo = correo.strip().lower()
        patron = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+$"

        if not re.fullmatch(patron, correo):
            raise ValueError("El correo electronico no es valido.")

        return correo

    @staticmethod
    def validar_telefono(telefono):
        if telefono is None or telefono == "":
            return None

        if not isinstance(telefono, str):
            raise ValueError("El telefono debe ser un texto numerico.")

        telefono = telefono.strip()

        if not telefono.isdigit() or len(telefono) != 10:
            raise ValueError("El telefono debe contener 10 numeros.")

        return telefono

    # Propiedades para consultar los datos
    @property
    def nombre(self):
        return self.__nombre

    @property
    def documento(self):
        return self.__documento

    @property
    def correo(self):
        return self.__correo

    @property
    def telefono(self):
        return self.__telefono

    # Actualizacion de datos
    def actualizar_datos(self, nombre=None, correo=None, telefono=None):
        nuevo_nombre = self.__nombre
        nuevo_correo = self.__correo
        nuevo_telefono = self.__telefono

        if nombre is not None:
            nuevo_nombre = self.validar_nombre(nombre)

        if correo is not None:
            nuevo_correo = self.validar_correo(correo)

        if telefono is not None:
            nuevo_telefono = self.validar_telefono(telefono)

        self.__nombre = nuevo_nombre
        self.__correo = nuevo_correo
        self.__telefono = nuevo_telefono

    def mostrar_informacion(self):
        return (
            f"Nombre: {self.__nombre}\n"
            f"Documento: {self.__documento}\n"
            f"Correo: {self.__correo}\n"
            f"Telefono: {self.__telefono or 'No registrado'}"
        )


class GestionClientes:
    """Administra los clientes registrados."""

    def __init__(self):
        self.__clientes = []

    def registrar_cliente(self, nombre, documento, correo, telefono=None):
        documento = Cliente.validar_documento(documento)

        if self.buscar_cliente(documento) is not None:
            raise ValueError("Ya existe un cliente con ese documento.")

        cliente = Cliente(nombre, documento, correo, telefono)
        self.__clientes.append(cliente)
        return cliente

    def buscar_cliente(self, documento):
        for cliente in self.__clientes:
            if cliente.documento == documento:
                return cliente
        return None

    def listar_clientes(self):
        return tuple(self.__clientes)

    def actualizar_cliente(self, documento, nombre=None,
                           correo=None, telefono=None):
        cliente = self.buscar_cliente(documento)

        if cliente is None:
            raise ValueError("El cliente no esta registrado.")

        cliente.actualizar_datos(nombre, correo, telefono)
        return cliente
