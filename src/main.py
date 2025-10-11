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
                    print("--- Current Guests ---")
                    hotel.print_data()
                    print("----------------------")
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
                    print(f"Searching for guest with key: {key}")
                    print(hotel.search(key))
                else:
                    print("Usage: s <key>")

            # deletion
            elif command == 'r':
                if len(parts) == 2:
                    key = int(parts[1])
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
                    hotel.manual_insert(n)
                elif opt == 'c':
                    print("Command Option")
                    print("  1       - walk in")
                    print("  2       - walk in (infinite)")
                    print("  3       - bus")
                    print("  4       - bus (infinite)")
                    channel = int(input("Enter insert channel: "))
                    match channel:
                        case 1:
                            # insert n guests
                            total_number = int(
                                input("Enter guest number: "))
                            hotel.walk_in(total_number)
                        case 2:
                            # insert infinite guest
                            total_number = int(
                                input("Enter guest number (infinite): "))
                            hotel.bus(1, total_number)
                        case 3:
                            # insert n buses
                            guest_per_bus = int(
                                input("Enter guest number per bus (infinite): "))
                            total_bus = int(input("Enter total bus: "))
                            hotel.bus(total_bus, guest_per_bus)
                        case 4:
                            # insert infinite bus
                            guests = int(
                                input("Enter guest number per bus (infinite): "))
                            buses = int(
                                input("Enter total bus (infinite): "))
                            hotel.ship(buses, guests)
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
