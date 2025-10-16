from hotel import Hotel
import os
import sys


def print_blackroom():
    print("""
██████╗  ██╗       █████╗   ██████╗ ██╗  ██╗ ██████╗   ██████╗   ██████╗  ███╗   ███╗
██╔══██╗ ██║      ██╔══██╗ ██╔════╝ ██║ ██╔╝ ██╔══██╗ ██╔═══██╗ ██╔═══██╗ ████╗ ████║
██████╔╝ ██║      ███████║ ██║      █████╔╝  ██████╔╝ ██║   ██║ ██║   ██║ ██╔████╔██║
██╔══██╗ ██║      ██╔══██║ ██║      ██╔═██╗  ██╔══██╗ ██║   ██║ ██║   ██║ ██║╚██╔╝██║
██████╔╝ ███████╗ ██║  ██║ ╚██████╗ ██║  ██╗ ██║  ██║ ╚██████╔╝ ╚██████╔╝ ██║ ╚═╝ ██║
╚═════╝  ╚══════╝ ╚═╝  ╚═╝  ╚═════╝ ╚═╝  ╚═╝ ╚═╝  ╚═╝  ╚═════╝   ╚═════╝  ╚═╝     ╚═╝
          """)


def goodbye():
    print("""

 ██████╗  ██████╗  ██████╗ ██████╗ ██████╗ ██╗   ██╗███████╗
██╔════╝ ██╔═══██╗██╔═══██╗██╔══██╗██╔══██╗╚██╗ ██╔╝██╔════╝
██║  ███╗██║   ██║██║   ██║██║  ██║██████╔╝ ╚████╔╝ █████╗  
██║   ██║██║   ██║██║   ██║██║  ██║██╔══██╗  ╚██╔╝  ██╔══╝  
╚██████╔╝╚██████╔╝╚██████╔╝██████╔╝██████╔╝   ██║   ███████╗
 ╚═════╝  ╚═════╝  ╚═════╝ ╚═════╝ ╚═════╝    ╚═╝   ╚══════╝
                                                                              

          """)


def print_help():
    print("Commands:")
    print("  q                    - Quit the program")
    print("  h                    - Help")
    print("  p                    - Print all guest data")
    print("  s <key>              - Search for a guest by key (room number)")
    print("  r <key>              - Remove a guest by key (room number)")
    print("  i                    - Insert guest")
    print("  w                    - write all guests data to file")
    print("--------------------------")


def clear_screen():
    try:
        os.system('cls' if os.name == 'nt' else 'clear')
    except Exception:
        sys.stdout.write('\033[2J\033[H')
        sys.stdout.flush()


def main():

    hotel = Hotel()
    clear_screen()
    print_blackroom()
    try:
        initial_number = int(input("Enter initialize amount: "))
        if initial_number <= 0:
            print('Initialize amount must be positive integer')
    except ValueError as e:
        print('number please !!!!')
        return
    print(f'initializing {initial_number} rooms')
    hotel.walk_in(initial_number, profile_msg="initialize")
    input(
        f"Initialize hotel {initial_number} room(s) finish: enter to continue ")
    clear_screen()
    print_blackroom()
    print_help()
    while True:
        try:
            inp = input("Enter Option: ").strip()
            if not inp:
                continue

            parts = inp.split(" ")
            command = parts[0].lower()

            if command == 'q':
                confirm = ''
                while confirm != 'y' and confirm != 'n':
                    confirm = input("Are you sure to quit [Y/N]: ").lower()

                if confirm == 'y':
                    clear_screen()
                    goodbye()
                    break

            elif command == 'h':
                print_help()

            elif command == 'p':
                if len(parts) == 1:
                    clear_screen()
                    print_blackroom()
                    hotel.print_data()
                else:
                    print("Usage: p")

            # write file
            elif command == 'w':
                if len(parts) == 1:
                    print("--- writing file ---")
                    hotel.get_file()
                else:
                    print("Usage: w")

            # searching
            elif command == 's':
                if len(parts) == 2:
                    key = int(parts[1])
                    if key <= 0:
                        print('Key must be positive interger')
                        continue
                    print(f"Searching for guest with key: {key}")
                    print(hotel.search(key))
                else:
                    print("Usage: s <key>")

            # deletion
            elif command == 'r':
                if len(parts) == 2:
                    key = int(parts[1])
                    if key <= 0:
                        print('Key must be positive interger')
                        continue
                    print(f"Removing guest with key: {key}")
                    print(hotel.remove(key))
                else:
                    print("Usage: r <key>")

            # insertion
            elif command == 'i':
                clear_screen()
                print_blackroom()
                print("Command Option")
                print("  m       - manual insert")
                print("  c       - select channel to insert")
                opt = input("Enter insertion method: ")
                # i m manual insert at key
                if opt == 'm':
                    n = int(input("Enter room number: "))
                    if n <= 0:
                        print('Room number must be positive integer')
                    else:
                        hotel.manual_insert(n)
                elif opt == 'c':
                    print("Command Option")
                    print("  1       - walk in")
                    print("  2       - walk in (infinite)")
                    print("  3       - bus (-c for custom number)")
                    print("  4       - bus (infinite) (-c for custom number)")
                    input_ch = input("Enter insert channel: ").strip()
                    channel = int(input_ch.split(" ")[0].strip())
                    flag = None
                    try:
                        flag = input_ch.split(" ")[1].strip()
                    except:
                        pass
                    match channel:
                        case 1:
                            # insert n guests
                            total_number = int(
                                input("Enter guest number: "))
                            if total_number <= 0:
                                print('Channel must be an positive integer')
                                continue
                            hotel.walk_in(total_number)
                        case 2:
                            # insert infinite guest
                            total_number = int(
                                input("Enter guest number (infinite): "))
                            if total_number <= 0:
                                print('number input must in positive integer')
                            else:
                                hotel.bus(1, [total_number], total_number, msg='walk in (infinity) logic',
                                          profile_msg='walk in (infinity) logic')
                        case 3:
                            # insert n buses (finite)
                            total_bus = int(input("Enter total bus: "))
                            if total_bus <= 0:
                                print('number input must be positive integer')
                                break
                            if flag is not None and flag == '-c':
                                # custom guests per bus list
                                guest_list = []
                                max_guest = 0
                                for idx in range(total_bus):
                                    while True:
                                        try:
                                            g = int(
                                                input(f"Enter guests for bus {idx + 1}: "))
                                            if g <= 0:
                                                print(
                                                    'number input must be positive integer')
                                                continue
                                            if g > max_guest:
                                                max_guest = g
                                            guest_list.append(g)
                                            break
                                        except ValueError:
                                            print('number please !!!!')
                                hotel.bus(total_bus, guest_list, max_guest, msg='bus (finite) logic',
                                          profile_msg='bus (finite) logic')
                            elif flag is None:
                                # uniform guests per bus
                                try:
                                    guest_per_bus = int(
                                        input("Enter guest number per bus: "))
                                except ValueError:
                                    print('number please !!!!')
                                    break
                                if guest_per_bus <= 0:
                                    print('number input must be positive integer')
                                    break
                                guest_list = [guest_per_bus] * total_bus
                                hotel.bus(total_bus, guest_list, guest_list[0], msg='bus (finite) logic',
                                          profile_msg='bus (finite) logic')
                            else:
                                print('incorrect usage channel -c')
                                continue
                        case 4:
                            # ship (infinite)
                            if flag is not None and flag == '-c':
                                try:
                                    total_bus = int(
                                        input("Enter total bus (infinite): "))
                                except ValueError:
                                    print('number please !!!!')
                                    break
                                if total_bus <= 0:
                                    print('number input must be positive integer')
                                    break
                                guest_list = []
                                for idx in range(total_bus):
                                    while True:
                                        try:
                                            g = int(
                                                input(f"Enter guests for bus {idx + 1} (infinite): "))
                                            if g <= 0:
                                                print(
                                                    'number input must be positive integer')
                                                continue
                                            guest_list.append(g)
                                            break
                                        except ValueError:
                                            print('number please !!!!')
                                max_guest = int(
                                    input('Enter max guest per bus: '))
                                hotel.ship(total_bus, guest_list, max_guest)
                            elif flag is None:
                                # uniform guests per bus
                                try:
                                    guests = int(
                                        input("Enter guest number per bus (infinite): "))
                                    buses = int(
                                        input("Enter total bus (infinite): "))
                                except ValueError:
                                    print('number please !!!!')
                                    break
                                if guests <= 0 or buses <= 0:
                                    print('number input must be positive integer')
                                    break
                                guest_list = [guests] * buses
                                hotel.ship(buses, guest_list, guest_list[0])
                            else:
                                print('incorrect usage channel -c')
                                continue
                        case _:
                            print('Invalid channel')
                else:
                    print("invalid option (c | m)")

            else:
                print(
                    f"Error: Unknown command '{command}' | try 'h' for more information")

        except ValueError:
            print(
                "Error: Invalid number provided for key or amount. Please enter integers.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


if __name__ == '__main__':
    main()
else:
    raise SyntaxError
