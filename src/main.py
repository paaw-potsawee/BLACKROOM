from hotel import Hotel
from tracking import profile
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


def print_help():
    print("Commands:")
    print("  q                    - Quit the program")
    print("  h                    - Help")
    print("  p                    - Print all guest data")
    print("  s <key>              - Search for a guest by key (room number)")
    print("  r <key>              - Remove a guest by key (room number)")
    print("  i                    - Insert guest")
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
    hotel.walk_in(initial_number)
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
                clear_screen()
                print('Goodbye!')
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

            # searching
            elif command == 's':
                if len(parts) == 2:
                    key = int(parts[1])
                    print(f"Searching for guest with key: {key}")
                    guest = hotel.search(key)
                    if guest:
                        print(f"Found: {guest}")
                    else:
                        print(f"Guest with key {key} not found.")
                else:
                    print("Usage: s <key> | -e")

            # deletion
            elif command == 'r':
                if len(parts) == 2:
                    key = int(parts[1])
                    print(f"Removing guest with key: {key}")
                    hotel.remove(key)
                    print(f"Guest with key {key} removed.")
                else:
                    print("Usage: r <key>")

            # insertion
            elif command == 'i':
                clear_screen()
                print_blackroom()
                print("  m       - manual insert")
                print("  c       - select channel to insert")
                opt = input("Enter insertion method: ")
                # i m manual insert at key
                if opt == 'm':
                    pass
                # i c insert by channel e.g., walk(1) bus(2) boat(3) plane(4)
                elif opt == 'c':
                    channel = int(input("Enter insert channel: "))
                    match channel:
                        case 1:
                            total_number = int(
                                input("Enter guest number: "))
                            hotel.walk_in(total_number)
                        case 2:
                            pass
                        case 3:
                            pass
                        case 4:
                            pass
                        case _:
                            print('Invalid channel')

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
