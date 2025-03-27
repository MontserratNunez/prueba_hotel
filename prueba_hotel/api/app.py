from flask import Flask, request, jsonify, render_template
from utils import *
import requests

app = Flask(__name__)
app.config["DEBUG"] = True
app.config["SECRET_KEY"] = "SECRET_KEY"

url = "http://127.0.0.1:5000"

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/hotels", methods=["GET", "POST"])
def hotels():
    hotel_list = get_all_hotels(create_instance_hotel())
    if request.method == "POST":
        return jsonify(hotel_list)
    return render_template("hotels.html", hotels = hotel_list)

@app.route("/hotel/<hotel_id>", methods=["GET", "POST"])
def hotel(hotel_id):
    info = get_hotel(hotel_id, create_instance_hotel(), "info")
    if request.method == "POST":
        return jsonify(info)
    return render_template("hotel.html", info = info)

@app.route("/hotel/<hotel_id>/rooms", methods=["GET", "POST"])
def rooms(hotel_id):
    rooms_list = get_hotel(hotel_id, create_instance_hotel(), "rooms")
    if request.method == "POST":
        return jsonify(rooms_list)

@app.route("/hotel/<hotel_id>/locations", methods=["GET", "POST"])
def locations(hotel_id):
    locations_list = get_hotel(hotel_id, create_instance_hotel(), "locations")
    if request.method == "POST":
        return jsonify(locations_list)

@app.route("/bus/<bus_num>", methods=["GET", "POST"])
def seats(bus_num):
    bus = get_bus(bus_num, create_instance_bus(), "passengers")
    if request.method == "POST":
        return jsonify(bus)
    return render_template("buses.html", rooms = rooms)

@app.route("/hotel/reservation", methods=["GET", "POST"])
def reservation():
    data = request.get_json()
    hotel_id = data.get("hotel_id")
    name = data.get("name")
    bus_number = data.get("bus_number")
    room_number = data.get("room_number")
    add_reservation_to_csv(hotel_id, name, room_number)
    insert_new("passengers", [hotel_id, name, bus_number, room_number])

    return jsonify({"message": "Reserva realizada exitosamente"}), 200

@app.route("/hotel/checkout", methods=["GET", "POST"])
def checkout_hotel():
    data = request.get_json()
    reservation_id = data.get("reservation_id")
    checkout(reservation_id)
    return jsonify({"message": "Checkout realizado exitosamente"}), 200

if __name__ == "__main__":
    app.run()