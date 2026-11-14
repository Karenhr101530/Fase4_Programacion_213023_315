from sistema import SistemaSoftwareFJ
from registro import logger


def main():
    # Crea el sistema e inicia la demostracion de operaciones.
    sistema = SistemaSoftwareFJ()
    print("=== SOFTWARE FJ - DEMOSTRACION DE OPERACIONES ===")

    # Ejecuta cada operacion y controla los errores sin detener el programa.
    def ejecutar(numero, descripcion, accion):
        print(f"\n{numero}. {descripcion}")
        try:
            resultado = accion()
        except Exception as error:
            # Registra el error en el archivo de logs.
            logger.error("Operacion %s fallida: %s", numero, error)
            print(f"Error controlado: {error}")
        else:
            # Muestra los detalles cuando la operacion devuelve una reserva.
            if hasattr(resultado, "obtener_detalles_reserva"):
                print(resultado.obtener_detalles_reserva())
            else:
                print("Operacion realizada correctamente.")
        finally:
            print("El sistema continua funcionando.")

    # Pruebas de registro y validacion de clientes.
    ejecutar(1, "Registrar cliente valido", lambda: sistema.registrar_cliente("Maria Lopez", "12345678", "maria@example.com"))
    ejecutar(2, "Registrar segundo cliente", lambda: sistema.registrar_cliente("Juan Perez", "87654321", "juan@example.com"))
    ejecutar(3, "Rechazar documento duplicado", lambda: sistema.registrar_cliente("Otra Persona", "12345678", "otra@example.com"))
    ejecutar(4, "Rechazar correo incorrecto", lambda: sistema.registrar_cliente("Ana Gomez", "98765432", "correo_malo"))

    # Pruebas de creacion y validacion de servicios.
    ejecutar(5, "Crear servicio de sala", lambda: sistema.agregar_servicio("sala", 50000, capacidad_maxima=10))
    ejecutar(6, "Crear servicio de equipos", lambda: sistema.agregar_servicio("equipo", 30000, inventario=3))
    ejecutar(7, "Crear servicio de asesoria", lambda: sistema.agregar_servicio("asesoria", 80000))
    ejecutar(8, "Rechazar servicio con tarifa negativa", lambda: sistema.agregar_servicio("sala", -100))
    ejecutar(9, "Rechazar tipo de servicio desconocido", lambda: sistema.agregar_servicio("otro", 20000))

    # Obtiene los servicios registrados para utilizarlos en las reservas.
    sala, equipo, asesoria = sistema.servicios

    # Crea una reserva y solicita su confirmacion.
    def confirmar(identificador, documento, servicio, horas, **opciones):
        reserva = sistema.crear_reserva(identificador, documento, servicio, horas)
        reserva.confirmar_reserva(**opciones)
        return reserva

    # Pruebas de reservas correctas e incorrectas.
    ejecutar(10, "Confirmar reserva de sala con descuento", lambda: confirmar("R01", "12345678", sala, 2, personas=4, descuento=10))
    ejecutar(11, "Confirmar alquiler de equipos", lambda: confirmar("R02", "87654321", equipo, 2, cantidad=2))
    ejecutar(12, "Confirmar asesoria presencial", lambda: confirmar("R03", "12345678", asesoria, 1, modalidad="presencial"))
    ejecutar(13, "Rechazar inventario insuficiente", lambda: confirmar("R04", "87654321", equipo, 2, cantidad=10))
    ejecutar(14, "Rechazar cliente no registrado", lambda: sistema.crear_reserva("R05", "11111111", sala, 2))
    ejecutar(15, "Rechazar reserva duplicada", lambda: sistema.crear_reserva("R01", "12345678", sala, 2))

    # Comprueba que una reserva cancelada no pueda confirmarse.
    def cancelar():
        reserva = sistema.crear_reserva("R06", "12345678", sala, 1)
        reserva.cancelar_reserva()
        reserva.confirmar_reserva()
        return reserva

    ejecutar(16, "Cancelar reserva y bloquear confirmacion", cancelar)

    print("\n=== DEMOSTRACION FINALIZADA: 16 OPERACIONES EJECUTADAS ===")
    print("Los eventos y errores se encuentran en sistema_errores.log.")


# Ejecuta el programa solamente cuando se abre este archivo directamente.
if __name__ == "__main__":
    main()