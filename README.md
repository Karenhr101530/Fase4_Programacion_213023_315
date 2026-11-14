SISTEMA INTEGRAL DE GESTIÓN DE CLIENTES, SERVICIOS Y RESERVAS

Universidad: Universidad Nacional Abierta y a Distancia (UNAD)
Curso: Programación (213023)
Grupo: 213023_315
Actividad: Fase 4 – Prácticas simuladas
Empresa ficticia: Software FJ

1. DESCRIPCIÓN DEL PROYECTO

Este proyecto colaborativo fue desarrollado en Python para la empresa ficticia Software FJ, con el propósito de crear un sistema que permita gestionar clientes, servicios y reservas mediante la aplicación de conceptos de programación orientada a objetos.

El sistema integra diferentes clases que permiten registrar clientes, administrar servicios, realizar reservas y calcular sus costos. También cuenta con validaciones y manejo de excepciones para controlar situaciones que puedan presentarse durante su funcionamiento.

La información se almacena temporalmente mediante listas en memoria, por lo que no se utiliza una base de datos.

2. FUNCIONALIDADES DEL SISTEMA

- Registro, consulta y validación de clientes.
- Identificación de clientes mediante documentos únicos.
- Gestión de reservas de salas, alquiler de equipos y asesorías especializadas.
- Creación, confirmación y cancelación de reservas.
- Cálculo de costos según las condiciones de cada servicio, incluyendo impuestos y descuentos.
- Validación de disponibilidad, capacidad y duración de las reservas.
- Manejo de excepciones personalizadas y registro de errores.
- Ejecución de operaciones válidas e inválidas para comprobar el funcionamiento del sistema.

3. ARCHIVOS DEL PROYECTO

El proyecto está organizado en los siguientes archivos:

- entidad.py: Contiene la clase abstracta general.
- cliente.py: Permite registrar, consultar y validar los datos de los clientes.
- services.py: Contiene los diferentes servicios, sus tarifas y cálculos de costos.
- reservas.py: Gestiona la creación, confirmación y cancelación de reservas.
- sistema.py: Integra las clases y permite realizar las operaciones del sistema.
- registro.py: Gestiona el registro de eventos y errores.
- main.py: Ejecuta las operaciones de demostración del programa.
- pruebas_integracion.py: Comprueba el funcionamiento conjunto de los módulos.
- pruebas_requisitos.py: Verifica requisitos específicos del sistema.
- .gitignore: Excluye archivos temporales y de registro del control de versiones.

4. CONCEPTOS DE PROGRAMACIÓN APLICADOS

Durante el desarrollo del proyecto se aplicaron diferentes conceptos de programación orientada a objetos:

- Abstracción: Mediante clases abstractas que permiten definir características y comportamientos generales.
- Herencia: Para reutilizar atributos y métodos entre clases relacionadas.
- Polimorfismo: Para implementar comportamientos específicos según el tipo de servicio.
- Encapsulación: Para proteger los atributos de los objetos y controlar el acceso a sus datos.
- Parámetros opcionales: Para permitir diferentes condiciones en las operaciones del sistema.
- Manejo de excepciones: Para controlar errores y evitar que las situaciones inválidas detengan inesperadamente el programa.

También se utilizaron las estructuras try, except, else y finally, junto con excepciones personalizadas y encadenamiento de excepciones.

5. VALIDACIONES Y REGISTRO DE ERRORES

El sistema cuenta con validaciones para evitar documentos repetidos, datos incorrectos, servicios no disponibles, capacidades excedidas y reservas que no cumplen las condiciones establecidas.

Además, se implementó un mecanismo de registro que guarda los eventos y errores relevantes en el archivo sistema_errores.log.

Este archivo se genera durante la ejecución cuando corresponde y no necesita incluirse en el repositorio de GitHub.

6. REQUISITOS Y EJECUCIÓN

Para ejecutar el proyecto se necesita Python 3. No es necesario instalar librerías externas adicionales.

El programa puede ejecutarse desde Visual Studio Code o desde una terminal ubicada en la carpeta del proyecto.

Para ejecutar el programa principal:

python main.py

Para ejecutar las pruebas automatizadas:

python -m unittest -v pruebas_integracion pruebas_requisitos

7. PRUEBAS REALIZADAS

Se desarrollaron 23 pruebas automatizadas, distribuidas de la siguiente manera:

- 18 pruebas de integración: Verifican el funcionamiento de los clientes, servicios, reservas, cálculos y validaciones.
- 5 pruebas de requisitos: Comprueban condiciones específicas, como clases abstractas, identificadores duplicados, clientes y servicios no registrados y encadenamiento de excepciones.

En la última ejecución se completaron las 23 pruebas correctamente, sin fallos.

También se incluyeron operaciones de demostración en main.py para observar el comportamiento del programa ante situaciones válidas e inválidas.

8. DESARROLLO COLABORATIVO

El proyecto se desarrolló de manera colaborativa mediante GitHub, utilizando ramas independientes para organizar los aportes de los integrantes del grupo.

- Clientes: Karen Hernández desarrolló el registro y la validación de clientes.
- Servicios: Juan Miguel desarrolló los diferentes servicios y sus cálculos.
- Reservas: Jhonatan desarrolló la gestión de reservas y sus estados.
- Integración: Se conectaron los módulos y se incorporaron las pruebas necesarias para comprobar el funcionamiento general del sistema.

Se utilizaron las ramas Clientes, Services y Reserva para el desarrollo de los módulos correspondientes, mientras que Integracion se destinó a reunir los componentes y comprobar su funcionamiento conjunto.

Los aportes realizados pueden consultarse mediante las ramas y el historial de commits del repositorio.
