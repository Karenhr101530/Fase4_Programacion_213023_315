from Services import ReservaSala, AlquilerEquipo, AsesoriaEspecializada

# Crear los tres servicios


sala = ReservaSala(
    50000,
    capacidad_maxima=20
)

equipo = AlquilerEquipo(
    30000,
    inventario=10
)

asesoria = AsesoriaEspecializada(
    80000
)

# Mostrar información de los servicios

print(sala.describir_servicio())
print(equipo.describir_servicio())
print(asesoria.describir_servicio())

print("\n--- PRUEBAS DE COSTOS ---")

# Costo de reservar una sala durante 2 horas
print("Costo de sala:", sala.calcular_costo(horas=2))

# Costo de alquilar 3 equipos durante 2 horas
print("Costo de equipos:", equipo.calcular_costo(horas=2, cantidad=3))

# Costo de una asesoría virtual durante 2 horas
print("Costo de asesoría:", asesoria.calcular_costo(horas=2, modalidad="virtual"))


print("\n--- PRUEBAS DE VALIDACIONES ---")

try:
    sala.calcular_costo(horas=-2)
except Exception as e:
    print("Error de sala:", e)

try:
    equipo.calcular_costo(horas=2, cantidad=15)
except Exception as e:
    print("Error de equipos:", e)

try:
    asesoria.calcular_costo(horas=2, modalidad="presencial")
    print("Asesoría presencial: cálculo correcto")
except Exception as e:
    print("Error de asesoría:", e)
    
    
print("\n--- PRUEBAS DE DESCUENTOS ---")

print(
    "Sala con 10% de descuento:",
    sala.calcular_costo(horas=2, descuento=10)
)

print(
    "Equipos con 20% de descuento:",
    equipo.calcular_costo(horas=2, cantidad=2, descuento=20)
)

print("\n--- PRUEBA DE DISPONIBILIDAD ---")

sala_no_disponible = ReservaSala(
    50000,
    capacidad_maxima=20,
    disponible=False
)

try:
    sala_no_disponible.calcular_costo(horas=2)
except Exception as e:
    print("Error de disponibilidad:", e)