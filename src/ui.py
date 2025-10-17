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
