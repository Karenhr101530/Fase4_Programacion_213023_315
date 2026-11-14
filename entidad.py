from abc import ABC, abstractmethod


class Entidad(ABC):
    # Base abstracta para las entidades del sistema.

    @abstractmethod
    def mostrar_informacion(self):
        # Devuelve los datos del cliente como texto.
        pass
