"""
vintage_car_db.py - A command-line tool for interacting with a vehicle database.

This script allows users to perform CRUD (Create, Read, Update, Delete) operations on a vintage car database.
It connects to a server hosting the database and provides a menu-driven interface to manage car data. 
Users can add, list, delete, or update car entries in the database using the provided options.

Usage:
    vintage_car_db.py <server_address> [port_number] [database] [cid]
    
Arguments:
    <server_address> (str): The address of the server hosting the vehicle database.
    [port_number] (int, optional): The port number for the server (default: 3000).
    [database] (str, optional): The name of the database to connect to (default: "vehicles").
    [cid] (str, optional): The car ID for specific operations such as delete or update (optional).

The script performs the following:
1. Validates input arguments including server address, port number, and database name.
2. Connects to the server and checks the database.
3. Presents the user with a menu of available operations:
    - List cars in the database
    - Add a new car entry
    - Delete a car entry by ID
    - Update an existing car entry by ID
4. Handles errors in communication with the server and input validation.

Exit Codes:
    1 - Incorrect arguments or invalid input
    2 - ValueError during argument validation
"""

import json
import requests
import vehicle_module as vm
import sys



if len(sys.argv) not in [2, 3, 4, 5]:
    print ("Usage: vintage_car_db.py, <server_address>, [port_number], [database], [cid]")
    sys.exit(1)

server_address = sys.argv[1]

default_port_number = 3000
default_database = "vehicles"
default_cid = None

try:
    port_number = int(sys.argv[2]) if len(sys.argv)> 2 else default_port_number
    if not (1 <= port_number <= 65536):
        raise ValueError (f'Port number musr be an  integer between 1 and 65536, but got {sys.argv[2]}')

    database = sys.argv[3] if len(sys.argv) > 3 else default_database
    cid = sys.argv[4] if len(sys.argv) == 5 else default_cid
    if cid and not cid.isdigit():
        raise ValueError (f'Car id must be mumeric integer.')
except ValueError as e:
    print (e)
    sys.exit (2)



while True:
    server_running, vehicle_data = vm.check_server(server_address, port_number, database)
    # if not vm.check_server(server_address, port_number, database):
    if not server_running:
        print("Server is not responding - quitting!")
        sys.exit (1)

    vm.print_menu ()
    choice = vm.read_user_choice ()
    if choice == "0":
        print ("You exit the program. Bye!")
        sys.exit (0)
    elif choice == "1":
        vm.list_cars (vehicle_data)
    elif choice  == "2":
        vm.add_car (server_address, port_number, database)
    elif choice == "3":
        vm.delete_car (server_address, port_number, database)
    elif choice == "4":
        vm.update_car (server_address, port_number, database)
    

















