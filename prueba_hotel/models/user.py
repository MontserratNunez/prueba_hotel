class User:
    """Creates a new user"""
    def __init__(self, name, password):
        self.name = name
        self.password = password

class Client(User):
    """Creates a new client"""
    def __init__(self, name, password):
        super().__init__(name, password)
        self.reservations = []

    def new_reservation(self):
        """Add a new reservation"""

    def get_reservations(self):
        """Returns all the reservations"""

class Admin(User):
    """Creates a new admin"""
    def __init__(self, name, password):
        super().__init__(name, password)
        self.permisions = []

    def add_hotel(self, hotel_id, hotel_name, address, phone):
        """Creates a new hotel to administrate"""
        #new_hotel = Hotel(hotel_id, hotel_name, address, phone)