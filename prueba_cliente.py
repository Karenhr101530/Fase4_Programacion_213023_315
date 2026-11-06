
from cliente import GestionClientes

gestion = GestionClientes()

# Pruebas de registro de clientes
pruebas = [
    ("Maria Perez", "123456789", "maria@gmail.com", "3001234567"),
    ("Juan Lopez", "987654321", "juan@gmail.com", None),
    ("", "111111111", "ana@gmail.com", None),
    ("Ana Torres", "123456789", "ana@gmail.com", None),
    ("Pedro Gomez", "555555555", "correo_invalido", None),
]

for nombre, documento, correo, telefono in pruebas:
    try:
        cliente = gestion.registrar_cliente(
            nombre, documento, correo, telefono
        )
    except ValueError as error:
        print(f"Error al registrar: {error}")
    else:
        print(f"Registrado correctamente: {cliente.nombre}")
    finally:
        print("Operacion finalizada.\n")

# Prueba de busqueda
print("BUSQUEDA DE CLIENTE")
cliente = gestion.buscar_cliente("123456789")

if cliente:
    print(cliente.mostrar_informacion())

# Prueba de actualizacion
print("\nACTUALIZACION DE CLIENTE")
try:
    cliente = gestion.actualizar_cliente(
        "123456789",
        correo="maria.nuevo@gmail.com"
    )
    print(cliente.mostrar_informacion())
except ValueError as error:
    print(f"Error: {error}")

# Lista de clientes registrados
print("\nLISTA DE CLIENTES")

for cliente in gestion.listar_clientes():
    print(cliente.mostrar_informacion())
    print("-------------------------")
