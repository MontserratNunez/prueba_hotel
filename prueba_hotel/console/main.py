import requests

url = "http://127.0.0.1:5000"
headers = {"X-API-KEY": "1234567890abcdef"}

def fetch(endpoint):
    """Collects the data from the api"""
    try:
        response = requests.post(url + endpoint, headers=headers, timeout=10,)
        if response.status_code == 200:
            data = response.json()
            return data
    except Exception:
        return "Error de conexion, inténtelo de nuevo"

def main():
    opcion = input("""1. Ver hoteles disponibles.",
"2. Consultar informacion de un hotel.",
"3. Ver habitaciones disponibles.",
"4. Reservar una habitacion.",
"5. Mostrar pasajeros de autobús.",
"6. Checkout.",
"7. Validar reserva y detalles de estadía.",
""")
        
    if opcion == "1":
        print_hotels()
    elif opcion == "2":
        hotel_id = input("Ingrese el ID de un hotel")
        print_hotel_info(hotel_id)
    elif opcion == "3":
        hotel_id = input("Ingrese el ID de un hotel")
        print_rooms(hotel_id)
    elif opcion == "4":
        hotel_id = input("Ingrese el ID de un hotel")
        room_num = input("Ingrese el número de habitación")
        reserve_room(hotel_id, room_num)
    elif opcion == "5":
        bus_num = input("Ingrese el número de autobús")
        print_passengers(bus_num)
    elif opcion == "6":
        num = input("Ingrese el número de la reserva")
        checkout(num)
    elif opcion == "7":
        num = input("Ingrese el número de la reserva")
        bus_num = input("Ingrese el número de autobús")
        validate_reservation(num, bus_num)
        
def print_multiples(opciones):
    for i, opcion in enumerate(opciones):
        print("=============================================")
        for j, (key, value) in enumerate(opcion.items()):
            print(f"{key} : {value}")
    print("=============================================")


def print_hotels():
    response = fetch("/hotels")
    hotel_dict = []
    for index, r in enumerate(response):
        hotel_dict.append({"Id": r[0], "Name": r[1]})
    print_multiples(hotel_dict)

def print_hotel_info(hotel_id):
    response = fetch(f"/hotel/{hotel_id}")
    print("=============================================")
    print(f"""Id": {response[0]},\n"Name": {response[1]},\n"Address": {response[2]},\n"Phone number": {response[3]}""")
    print("=============================================")

def print_rooms(hotel_id):
    response = fetch(f"/hotel/{hotel_id}/rooms")
    dict_values = []
    for index, room in enumerate(response):
        dict_values.append({"Numero de habitacion": room[1],"Tipo": room[0],"Precio": room[2]})
    print_multiples(dict_values)

def print_passengers(bus_num):
    response = fetch(f"/bus/{bus_num}")
    dict_passenger = []
    for index, passenger in enumerate(response):
        dict_passenger.append({"Nombre": passenger[0],"Número de autobús": passenger[1],"Número de habitación": passenger[2]})
    print_multiples(dict_passenger)

def reserve_room(hotel_id, room_number):
    name = input("Ingrese su nombre: ")
    bus_number = input("Ingrese el número de autobús: ")
    start_date = input("Ingrese la fecha de entrada (dd/mm/yy): ")
    end_date = input("Ingrese la fecha de salida (dd/mm/yy): ")
    
    reservation_data = {
        "hotel_id": hotel_id,
        "name": name,
        "bus_number": bus_number,
        "room_number": room_number,
        "start_date": start_date,
        "end_date": end_date
    }

    response = requests.post(url + "/hotel/reservation", headers=headers, json=reservation_data)
    
    if response.status_code == 200:
        data = response.json()
        print("Reserva realizada exitosamente!")
        print("=========================================")
        print(f"Hotel ID: {hotel_id}")
        print(f"Número de habitación: {room_number}")
        print(f"Desde: {start_date} hasta {end_date} ({data[2]['days']} dias)")
        print("-----------------------------------------")
        print(f"Precio total: {data[1]['total_price']}$")
        print("=========================================")

def checkout(reservation_id):
    response = requests.post(url + "/hotel/checkout", headers=headers, json={"reservation_id": reservation_id})
    
    if response.status_code == 200:
        print("Checkout realizado exitosamente!")

def validate_reservation(reservation_id, bus_num):
    """Permite al usuario validar una reserva ingresando el ID de la reserva."""
    response = requests.post(url + "/hotel/reservation/validate", headers=headers, json={"reservation_id": reservation_id})
    data = response.json()
    if response:
        print(f"La reserva con ID {reservation_id} es válida.")
        print("=========================================")
        print(f"Hotel ID: {data['hotel']}")
        print(f"Cliente: {data['client']}")
        print(f"Número de habitación: {data['room']}")
        print(f"Desde: {data['start']} hasta {data['end']}")
        print("=========================================")
    else:
        print(f"La reserva con ID {reservation_id} no es válida.")

if __name__ == "__main__":
    main()

#python console\main.py
