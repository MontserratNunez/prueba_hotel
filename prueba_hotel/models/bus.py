"""Module of the class bus"""
class Bus:
    """Creates a new bus"""

    class Passenger:
        """Creates a new passenger of the bus"""

        def __init__(self, passenger_name, bus_num, reservation_num):
            self.passenger_name = passenger_name
            self.bus_num = bus_num
            self.reservation_num = reservation_num

        def get_info(self):
            """Returns the info of the passenger"""
            return [self.passenger_name, self.bus_num, self.reservation_num]

    class Route:
        """Creates a new route of the bus"""
        def __init__(self, bus_num, route_num, street, schedule):
            self.bus_num = bus_num
            self.route_num = route_num
            self.street = street
            self.schedule = schedule

        def get_info(self):
            """Returns the info of the route"""
            return [self.bus_num, self.route_num, self.street, self.schedule]

    def __init__(self, num, available_seats, taken_seats):
        self.num = num
        self.available_seats = available_seats
        self.taken_seats = taken_seats
        self.routes = []
        self.passengers = []

    def get_info(self):
        """Returns the info of the bus"""
        return [self.num, self.available_seats, self.taken_seats]

    def get_routes(self):
        """Returns all the routes of the bus"""
        return [route.get_info() for route in self.routes]

    def get_passengers(self):
        """Returns all the passengers of the bus"""
        return [passenger.get_info() for passenger in self.passengers]

    def add_route(self, bus_num, route_num, street, schedule):
        """Add a new route to the bus"""
        route = self.Route(bus_num, route_num, street, schedule)
        self.routes.append(route)

    def add_passenger(self, passenger_name, bus_num, reservation_num):
        """Add a new passenger to the bus"""
        passenger = self.Passenger(passenger_name, bus_num, reservation_num)
        self.passengers.append(passenger)

