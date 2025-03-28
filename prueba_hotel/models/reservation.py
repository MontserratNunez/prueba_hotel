"""Module of the class reservation"""
class Reservation:
    """Creates a new reservation"""
    def __init__(self,reservation_id, hotel_id, client_name, room_num, start_date, end_date):
        self.reservation_id = reservation_id
        self.hotel_id = hotel_id
        self.client_name = client_name
        self.room_num = room_num
        self.start_date = start_date
        self.end_date = end_date

    def get_info(self):
        """Returns the information of the reservation"""
        return [self.hotel_id, self.client_name, self.room_num, self.reservation_id, self.start_date, self.end_date]
