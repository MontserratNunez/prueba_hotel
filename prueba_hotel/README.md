# Prueba Hotel

Este es un sistema de para realizar reservas de hotel. El usuario puede realizar reservas, consultar información de hoteles y realizar checkouts.

## Funcionalidades

1. **Ver hoteles disponibles**: Muestra una lista de hoteles disponibles.
2. **Consultar información de un hotel**: Muestra detalles sobre un hotel específico.
3. **Ver habitaciones disponibles**: Muestra las habitaciones disponibles de un hotel.
4. **Reservar una habitación**: Permite realizar una reserva en una habitación de un hotel.
5. **Mostrar pasajeros de autobús**: Muestra una lista de los pasajeros de un autobús específico.
6. **Checkout**: Realiza el checkout de una reserva y actualiza el estado de la habitación.

## Estructura del Proyecto

El proyecto está dividido en varias carpetas:

- **api**: Contiene la API creada con Flask, donde se manejan las solicitudes y respuestas del sistema.
  - `app.py`: El archivo principal de la API.
  - `utils.py`: Contiene funciones para organizar y gestionar la información.
- **console**: Contiene el archivo `main.py`, que interactúa con el usuario a través de la consola y hace uso de la API.
- **db**: Contiene la base de datos en archivos CSV (`buses.csv`, `hotels.csv`, `passengers.csv`, `reservations.csv`, `rooms.csv`), y un archivo `connect.py` para leer y escribir en los archivos CSV.
- **models**: Contiene los modelos de datos utilizados para la gestión de reservas, habitaciones y otros elementos del sistema.
