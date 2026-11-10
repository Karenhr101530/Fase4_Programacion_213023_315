¿Qué desarrollé?

Mi aporte al proyecto fue el módulo de Servicios, desarrollado en Python en el archivo services.py.

La idea de este módulo es representar los servicios que ofrece la empresa Software FJ. Es como si un asesor le estuviera explicando al público qué servicios tiene disponibles: reserva de salas, alquiler de equipos y asesorías especializadas.

Cada uno de estos servicios tiene sus propias características y condiciones.

¿Cómo funciona?

Además de mostrar los servicios disponibles, el programa realiza diferentes procesos internamente, como calcular los costos, aplicar descuentos e impuestos, validar los datos ingresados y comprobar que los servicios estén disponibles.

Por ejemplo, si un cliente solicita una sala durante dos horas, el sistema calcula el precio correspondiente. Si alguien intenta solicitar horas negativas o alquilar más equipos de los disponibles, el programa detecta el error y evita que la operación se realice incorrectamente.

¿Cómo realicé las pruebas?

Para comprobar que mi código funcionara, creé un segundo archivo llamado prueba_servicios.py.

En este archivo simulé ser un cliente que solicita diferentes servicios y proporciona datos al sistema. De esta manera pude probar situaciones normales y también situaciones incorrectas.

Realicé pruebas de:

Creación y descripción de los tres servicios.

Cálculo de costos e impuestos.

Aplicación de descuentos.

Validación de horas negativas.

Control del inventario de equipos.

Comprobación de disponibilidad de los servicios.

Las pruebas realizadas dieron los resultados esperados.