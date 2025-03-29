import sys
import os
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from db import connect
from models.hotel import Hotel
from models.bus import Bus
from models.reservation import Reservation

all_hotels = connect.read("hotels")
all_rooms = connect.read("rooms")
all_locations = connect.read("locations")
all_buses = connect.read("buses")
all_passengers = connect.read("passengers")
all_routes = connect.read("routes")
all_reservations = connect.read("reservations")

def insert_new(name, values):
    connect.append(name, values)

def checkout(reservation_id):
    """ Elimina la reserva y actualiza el estado de la habitación a "disponible"."""
    all_reservations = connect.read("reservations")
    reservation_to_remove = None
    room_to_update = None

    for reservation in all_reservations:
        if int(reservation["ID_RESERVATION"]) == int(reservation_id):
            reservation_to_remove = reservation
            room_to_update = {
                "ID_HOTEL": reservation["ID_HOTEL"],
                "ROOM_NUM": reservation["ROOM_NUM"]
            }
            break

    if reservation_to_remove is None:
        print("Reserva no encontrada.")
        return

    all_reservations.remove(reservation_to_remove)

    write_header_reservations = ["ID_RESERVATION", "ID_HOTEL", "NAME", "ROOM_NUM"]
    connect.write("reservations", write_header_reservations)
    for reservation in all_reservations:
        connect.append("reservations", [reservation["ID_RESERVATION"], reservation["ID_HOTEL"], reservation["NAME"], reservation["ROOM_NUM"]])

    update_room_status(room_to_update["ID_HOTEL"], room_to_update["ROOM_NUM"], "Disponible")

def create_instance_hotel():
    hotels_list = []
    for hotel in all_hotels:
        hotels_list.append(Hotel(hotel["ID_HOTEL"], hotel["NAME"], hotel["ADDRESS"], hotel["PHONE"]))

    create_instance_room(hotels_list)
    create_instance_location(hotels_list)

    return hotels_list

def create_instance_room(hotels_list):
    for hotel in hotels_list:
        for room in all_rooms:
            if hotel.hotel_id == room["ID_HOTEL"]:
                hotel.add_room(room["ID_ROOM"], room["TYPE"], room["NUMBER"], room["PRICE"], room["STATUS"])

def create_instance_location(hotels_list):
    for hotel in hotels_list:
        for location in all_locations:
            if hotel.hotel_id == location["ID_HOTEL"]:
                hotel.add_location(location["NAME"], location["TYPE"], location["INFO"])

def create_instance_bus():
    bus_list = []
    for bus in all_buses:
        bus_list.append(Bus(bus["BUS_NUM"], bus["AVAILABLE_SEATS"], bus["TAKEN"]))

    create_instance_passenger(bus_list)
    create_instance_route(bus_list)

    return bus_list

def create_instance_passenger(bus_list):
    for bus in bus_list:
        for passenger in all_passengers:
            if bus.num == passenger["BUS_NUM"]:
                bus.add_passenger(passenger["NAME"], passenger["BUS_NUM"], passenger["RESERVATION_NUMBER"])

def create_instance_route(bus_list):
    for bus in bus_list:
        for route in all_routes:
            if bus.num == route["BUS_NUM"]:
                bus.add_route(route["BUS_NUM"], route["ROUTE_NUM"], route["STREET"], route["SCHEDULE"])

def create_instance_reservation():
    reservations_list = []
    for reservation in all_reservations:
        reservations_list.append(Reservation(reservation["ID_RESERVATION"], reservation["ID_HOTEL"], reservation["NAME"], 
                                             reservation["ROOM_NUM"], reservation["START"],reservation ["END"]))
    return reservations_list

def get_all_hotels(hotels_list):
    info = [hotel.display() for hotel in hotels_list]
    return info

def get_hotel(hotel_id, hotels_list, command):
    for hotel in hotels_list:
        if hotel.hotel_id == hotel_id:
            match command:
                case "info":
                    return hotel.get_information()
                case "rooms":
                    return hotel.get_rooms()
                case "locations":
                    return hotel.get_locations()
    return "El ID ingresado no es válido"

def get_bus(num, bus_list, command):
    print(num, "utils.py")
    for bus in bus_list:
        print(bus.num)
        if bus.num == num:
            match command:
                case "info":
                    return bus.get_info()
                case "routes":
                    return bus.get_routes()
                case "passengers":
                    return bus.get_passengers()
    return "El número de bus ingresado no es válido"

def get_all_reservations(reservations_list):
    info = [reservation.get_info() for reservation in reservations_list]
    return info

def add_reservation(hotel_id, client_name, room_num, start_date, end_date):
    reservations = create_instance_reservation()

    start_date = datetime.strptime(start_date, "%Y-%m-%d").strftime("%d/%m/%Y")
    end_date = datetime.strptime(end_date, "%Y-%m-%d").strftime("%d/%m/%Y")

    for res in reservations:
        if res.hotel_id == hotel_id and res.room_num == room_num:
            existing_start = datetime.strptime(res.start_date, "%d/%m/%Y")
            existing_end = datetime.strptime(res.end_date, "%d/%m/%Y")
            new_start = datetime.strptime(start_date, "%d/%m/%Y")
            new_end = datetime.strptime(end_date, "%d/%m/%Y")

            if not (new_end <= existing_start or new_start >= existing_end):
                print("La habitación ya está reservada en estas fechas.")
                return
            
    rooms = connect.read("rooms")
    price_per_night = 0
    for room in rooms:
        if room["ID_HOTEL"] == hotel_id and room["NUMBER"] == room_num:
            price_per_night = float(room["PRICE"])
            break

    num_days = (datetime.strptime(end_date, "%d/%m/%Y") - datetime.strptime(start_date, "%d/%m/%Y")).days
    total_price = num_days * price_per_night
    add_reservation_to_csv(hotel_id, client_name, room_num, start_date, end_date)
    return total_price, num_days

def add_reservation_to_csv(hotel_id, client_name, room_num, start_date, end_date):
    reservations = get_all_reservations(create_instance_reservation())

    last_id = int(reservations[-1][3])
    reservation_id = last_id + 1
    create_instance_room(create_instance_hotel())
    connect.append("reservations", [reservation_id, hotel_id, client_name, room_num, start_date, end_date])

    update_room_status(hotel_id, room_num, "Reservada")

def update_room_status(hotel_id, room_num, new_status):
    """Actualiza el estado de la habitacion a 'Disponible' o 'Reservada'"""
    rooms = connect.read("rooms")
    for room in rooms:
        if int(room["ID_HOTEL"]) == int(hotel_id) and int(room["NUMBER"]) == int(room_num):
            room["STATUS"] = new_status
    
    write_header = ["ID_HOTEL", "ID_ROOM", "TYPE", "NUMBER", "PRICE", "STATUS"]

    connect.write("rooms", write_header)
    for room in rooms:
        connect.append("rooms", [room["ID_HOTEL"], room["ID_ROOM"], room["TYPE"], room["NUMBER"], room["PRICE"], room["STATUS"]])

def get_reservation_by_id(reservation_id):
    """Busca una reserva por su ID en reservations.csv"""
    reservations = create_instance_reservation()
    for res in reservations:
        if int(res.reservation_id) == int(reservation_id):
            return res.get_info()
    return None

def get_route_by_hotel(hotel_id):
    """Busca las rutas de autobuses que coincidan con la calle del hotel"""
    hotel_info = get_hotel(hotel_id, create_instance_hotel(), "info")
    street = hotel_info[2]
    buses = create_instance_bus()
    routes = []
    routes_on_hotels = []

    for bus in buses:
        routes.append(get_bus(bus.num, buses, "routes"))

    for route in routes:
        for r in route:
            if r[2] == street:
                routes_on_hotels.append(r)

    return routes_on_hotels


    

