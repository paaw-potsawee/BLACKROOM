from BPlusTree import BPlusTree
from tracking import profile
from tqdm import tqdm


class Guest:
    __slots__ = ('__id')

    def __init__(self, channel: int, arrived_order: int):
        self.__id = self.__get_id(channel, arrived_order)

    @property
    def id(self): return self.__id

    @staticmethod
    def __get_id(channel, arrived_order):
        ch = {0: 'INT_INF', 1: 'WLK_FIN', 2: 'WLK_INF', 3: 'BUS_FIN',
              4: 'BUS_INF', 5: 'MAN_FIN'}.get(channel, f'CH{channel}')
        return f"{ch}-{arrived_order:03d}"

    def __repr__(self) -> str:
        return f'{self.__id}'


class Hotel:
    __slots__ = ('__tree', '__guest_order')

    def __init__(self):
        self.__tree = BPlusTree(order=128)
        self.__guest_order = 0

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
    @profile(message='walk in logic')
    def walk_in(self, n, profile_msg: str | None = None):
        # initial build (bulk load)
        if (profile_msg == "initialize") or self.__tree.is_empty():
            pairs = [(i, Guest(0, self.__guest_order))
                     for i in range(1, n + 1)]
            self.__tree.bulk_load(pairs)
            self.__guest_order += 1
            return

        self.__tree.process_room_number(lambda x: x + n)
        for i in tqdm(range(1, n + 1)):
            guest = Guest(1, self.__guest_order)
            self.__tree.insert((i, guest))
        self.__guest_order += 1

    # bus (conceptually infinity guests on n bus)
    @profile
    def bus(self, total_bus: int, guest_in_bus: list[int], max_guest: int, profile_msg: str | None = None):
        self.__tree.process_room_number(
            lambda x: x * (total_bus + 1))
        guest_channel = 2 if profile_msg != 'bus (finite) logic' else 3
        for guest in range(1, max_guest + 1):
            for bus in range(1, total_bus + 1):
                print(bus, guest)
                if guest_in_bus[bus - 1] > 0:
                    room = ((guest * (total_bus + 1)) - bus)
                    self.__tree.insert(
                        (room, Guest(guest_channel, self.__guest_order)))
                    guest_in_bus[bus - 1] -= 1
        # for i in tqdm(range(1, guest_per_bus + 1)):
        #     for bus_no in range(1, total_bus + 1):
        #         guest_no = ((i * (total_bus + 1)) - bus_no)
        #         guest = Guest(guest_channel, self.__guest_order)
        #         self.__tree.insert((guest_no, guest))

        self.__guest_order += 1

    @profile(message='bus (infinite) logic')
    def ship(self, total_bus: int, guest_in_bus: list[int], sum_val: int):
        # Apply triangular transform: tri(x) = x*(x+1)//2
        self.__tree.process_room_number(lambda x: (((x + 1) * (x)) // 2))
        bus = 1
        guest = 1
        max_value = 1
        sum_val = sum(guest_in_bus)
        while sum_val > 0:
            guest = 1
            bus = max_value
            while bus > 0 and bus <= max_value and guest > 0 and guest <= max_value:
                if bus <= total_bus and guest_in_bus[bus - 1] > 0:
                    guest_no = ((bus + guest) *
                                (bus + guest - 1)) // 2 + guest
                    guest_class = Guest(4, self.__guest_order)
                    self.__tree.insert((guest_no, guest_class))
                    guest_in_bus[bus - 1] -= 1
                    sum_val -= 1
                guest += 1
                bus -= 1
            max_value += 1
        self.__guest_order += 1

    @profile(message='manual insertion')
    def manual_insert(self, key):
        # insert at specific room if guest exists will replace that guest
        guest = Guest(5, self.__guest_order)
        self.__tree.insert((key, guest))
        self.__guest_order += 1

    @profile(message='fetch all guest')
    def print_data(self):
        print("--- Current Guests ---")
        self.__tree.print_leaf()
        print("----------------------")

    @profile
    def search(self, key):
        result = self.__tree.search(key)
        if result == -1:
            return f"room {key} is empty"

        return f"found: {result}-{key:09d}"

    @profile
    def remove(self, key):
        removed = self.__tree.delete(key)
        if removed == -1:
            return f"room {key} is not occupied"
        return f"room {key} removed"

    def get_file(self):
        self.__tree.export_to_csv()


if __name__ == "__main__":
    h = Hotel()
    h.walk_in(5, 'initialize')
    h.print_data()
    lst = [4, 5, 6]
    h.bus(3, lst, 6)
    h.print_data()
