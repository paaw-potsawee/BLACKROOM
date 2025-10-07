from hotel import Hotel
from tracking import profile


def print_help():
    print("""
██████╗  ██╗       █████╗   ██████╗ ██╗  ██╗ ██████╗   ██████╗   ██████╗  ███╗   ███╗
██╔══██╗ ██║      ██╔══██╗ ██╔════╝ ██║ ██╔╝ ██╔══██╗ ██╔═══██╗ ██╔═══██╗ ████╗ ████║
██████╔╝ ██║      ███████║ ██║      █████╔╝  ██████╔╝ ██║   ██║ ██║   ██║ ██╔████╔██║
██╔══██╗ ██║      ██╔══██║ ██║      ██╔═██╗  ██╔══██╗ ██║   ██║ ██║   ██║ ██║╚██╔╝██║
██████╔╝ ███████╗ ██║  ██║ ╚██████╗ ██║  ██╗ ██║  ██║ ╚██████╔╝ ╚██████╔╝ ██║ ╚═╝ ██║
╚═════╝  ╚══════╝ ╚═╝  ╚═╝  ╚═════╝ ╚═╝  ╚═╝ ╚═╝  ╚═╝  ╚═════╝   ╚═════╝  ╚═╝     ╚═╝
          """)
    print("Commands:")
    print("  q                    - Quit the program")
    print("  h                    - Help")
    print("  p                    - Print all guest data")
    print("  s <key> | -e         - Search for a guest by key (room number) or -e for empty room")
    print("  r <key>              - Remove a guest by key (room number)")
    print("  i -c | -m            - Insert guest, -m for manual -c for select channel")
    print("--------------------------")


def main():

    hotel = Hotel()
    print_help()
    while True:
        try:
            inp = input("Enter Option: ").strip()
            if not inp:
                continue

            parts = inp.split(" ")
            command = parts[0].lower()

            if command == 'q':
                print('Goodbye!')
                break

            elif command == 'h':
                print_help()

            elif command == 'p':
                if len(parts) == 1:
                    print("--- Current Guests ---")
                    hotel.print_data()
                    print("----------------------")
                else:
                    print("Usage: p")

            # searching
            elif command == 's':
                if len(parts) == 2:
                    if parts[1] == '-e':
                        print('Searching for all empty room')
                        empty_room = hotel.search_empty_room()
                        if empty_room:
                            print(
                                f"List of empty rooms in hotel: {empty_room}")
                        else:
                            print("No emptty room")
                    else:
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
                if len(parts) == 2:
                    opt = parts[1]
                    # i -m manual insert at key
                    if opt == '-m':
                        pass
                    # i -c insert by channel e.g., walk(1) bus(2) boat(3) plane(4)
                    elif opt == '-c':
                        channel = int(input("Enter insert channel: "))
                        match channel:
                            case 1:
                                pass
                            case 2:
                                pass
                            case 3:
                                pass
                            case 4:
                                pass
                            case _:
                                print('Invalid channel')
                else:
                    print("Usage: i -c | -m")

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
