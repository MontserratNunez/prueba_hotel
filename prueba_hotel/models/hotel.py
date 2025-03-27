"""Module of the class hotel"""

class Hotel:
    """Creates a new hotel"""

    class Room:
        """Creates a new room in thehotel"""

        def __init__(self, hotel_id, room_id, type_room, num_room, price, status):
            self.room_id = room_id
            self.hotel_id = hotel_id
            self.num_room = num_room
            self.type_room = type_room
            self.price = price
            self.status = status

        def get_info(self):
            """Returns the info of the room"""
            return [self.type_room, self.num_room, self.price, self.status]
        
    class Location:
        """Creates a new location in a hotel"""

        def __init__(self, hotel_id, location_name, location_type, location_info):
            self.hotel_id = hotel_id
            self.location_name = location_name
            self.location_type = location_type
            self.location_info = location_info

        def get_info(self):
            """Returns the info of the location"""
            return [self.location_name, self.location_type, self.location_info]

    def __init__(self, hotel_id, hotel_name, address, phone):
        self.hotel_id = hotel_id
        self.hotel_name = hotel_name
        self.address = address
        self.phone = phone
        self.about = ""
        self.rooms = []
        self.locations = []

    def display(self):
        """Returns the basic information of the hotel"""
        return [self.hotel_id, self.hotel_name]

    def get_information(self):
        """Returns all the information of the hotel"""
        return [self.hotel_id, self.hotel_name, self.address, self.phone, self.about]

    def get_rooms(self):
        """Returns the rooms of the hotel"""
        return [room.get_info() for room in self.rooms]

    def get_locations(self):
        """Returns the locations of the hotel"""
        return [location.get_info() for location in self.locations]

    def add_about(self, description):
        self.about = description

    def add_room(self, room_id, type_room, num_room, price, status):
        """Adds a new room to the hotel"""
        new_room = self.Room(self.hotel_id, room_id, type_room, num_room, price, status)
        self.rooms.append(new_room)

    def add_location(self, name, location_type, location_info):
        """Adds a new location to the hotel"""
        new_location = self.Location(self.hotel_id, name, location_type, location_info)
        self.locations.append(new_location)

