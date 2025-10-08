from BPlusTree import BPlusTree
from tracking import profile


class Guest:
    def __init__(self, current_room_number: int, channel: int, arrived_order: int):
        self.__current_room_number = current_room_number
        self.__channel = channel
        self.__arrived_order = arrived_order

    @property
    def current_room_number(self): return self.__current_room_number
    @current_room_number.setter
    def current_room_number(self, n): self.__current_room_number = n

    @property
    def channel(self): return self.__channel

    @property
    def arrived_order(self): return self.__arrived_order

    def __repr__(self) -> str:
        return f"Guest(Room: {self.__current_room_number}, Channel: {self.channel}, Arrived: {self.__arrived_order})"


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
    # walk in shift current guest by number of new guests
    @profile
    def walk_in(self, n):
        self.__tree.process_room_number(lambda x: x + n)
        # insert new guests
        for i in range(n):
            guest = Guest(i, 1, self.__guest_order)
            self.__tree.insert((i, guest))

        self.__guest_order += 1

    # bus (conceptually infinity guests on n bus)
    def bus(self, total_bus, guest_per_bus):
        self.__tree.process_room_number(lambda x: x * (total_bus + 1))
        for bus_no in range(1, total_bus + 1):
            for i in range(guest_per_bus):
                guest_no = (i * (total_bus + 1) + bus_no)
                guest = Guest(guest_no, 2, self.__guest_order)
                self.__tree.insert((guest_no, guest))

        self.__guest_order += 1

    def ship(self, guest_per_ship, guest_per_bus):
        self.__tree.process_room_number(lambda x: int(((x - 1) * (x)) / 2 + x))
        for bus in range(1, guest_per_bus + 1):
            for i in range(1, guest_per_ship + 1):
                guest_no = int(((bus + i - 1) * (bus + i)) / 2 + i)
                guest = Guest(guest_no, 3, self.__guest_order)
                self.__tree.insert((guest_no, guest))

        self.__guest_order += 1

    def print_data(self):
        self.__tree.print_leaf()

    def search(self, key):
        return self.__tree.search(key)

    def remove(self, key):
        self.__tree.delete(key)

    def get_file(self):
        pass


if __name__ == "__main__":
    hotel = Hotel()
    hotel.walk_in(50)
    hotel.ship(2, 10)
    # hotel.bus(4, 10)
    hotel.print_data()
