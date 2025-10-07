from BPlusTree import BPlusTree
from tracking import profile


class Guest:
    def __init__(self, current_room_number: int, channel: int, arrived_order: int):
        self.__current_room_number = current_room_number
        self.__channel = channel
        self.__arrived_order = arrived_order

    @property
    def current_room_number(self): return self.__current_room_number

    @property
    def channel(self): return self.__channel

    @property
    def arrived_order(self): return self.__arrived_order

    def __repr__(self) -> str:
        return f"Guest(Room: {self.__current_room_number}, Channel: {self.channel} ,Arrived: {self.__arrived_order}"


class Hotel:
    def __init__(self):
        self.__tree = BPlusTree()
        self.__guest_order = 0
        self.__max_guest_room = 0

    """
        1. insert guest by channel and total amount
        2. manage current guest and new guest (move to n room number etc...)
        3. can accept more guest (conceptually infinite)
        4. add guest at specific key
        5. delete guest at specific key
        6. can sort room number
        7. can search by room number
        8. show time usage in each function
        9. show space usage for this hotel
        10. in hotel can store channel (how they arrived), order (order when they arrived), room number (key from BPlus tree)
        11. write result as file
    """

    # insertion method
    # walk in (conceptually infinity guests)
    def walk_in(self, n):
        pass

    # bus (conceptually infinity guests on n bus)
    def bus(self, n, guest_per_bus):
        pass

    def print_data(self):
        pass

    def search(self, key):
        pass

    def remove(self, key):
        pass

    def get_file(self):
        pass

    def search_empty_room(self):
        pass
