from BPlusTree import BPlusTree

class Room:
    def __init__(self, room_number: int):
        self.__room_number = room_number
        self.__is_available = True
        
    def add_booking(self):
        if self.__is_available:
            self.__is_available = False
            return True
        return False
    
    def remove_booking(self):
        if not self.__is_available:
            self.__is_available = True
            return True
        return False
    
    @property
    def is_available(self):
        return self.__is_available

    @property
    def room_number(self):
        return self.__room_number
    
    def __str__(self):
        return f'Room {self.__room_number}, Available: {self.__is_available}'
    

class Hotel:
    def __init__(self):
        self.__room = BPlusTree() 
        self.__count = 0
    
    def add_room(self, room_number: int):
        if self.__room.search_value(room_number) is None:
            room_number = Room(room_number)
            self.__room.insert(self.__count, room_number)
            self.__count += 1
            return True
        return False
    
    def book_room(self, room_number: int):
        room_key = self.__room.search_value(room_number)
        if room_key is not None:
            return True
        return False

    def cancel_booking(self, room_number: int):
        room_key = self.__room.search_value(room_number)
        if room_key is not None:
            return True
        return False

    @property
    def room_count(self):
        return self.__count
    
    def print_tree(self):
        self.__room.print_tree()



h = Hotel()
for i in range(0 , 99999):
    h.add_room(i)
    


h.print_tree()