import requests
import json

""" This module comprises of all the functions to manage small database that gathers data 
    about the vintage cars. 
"""
# Funtion to print menu.
def print_menu ():
    """ This function prints the header and the menu of the application"""
    # Print header.
    print ("+"+"-"*50 +"+")
    print ("|              Vintage Cars Database               |")
    print ("+"+"-"*50 +"+")
    # Print main menu.
    print ("M E N U")
    print("="*7)
    print ("1. List cars")
    print ("2. Add new car")
    print ("3. Delete car")
    print ("4. Update car")
    print ("0. Exit")


# Function to take user input for menu and validate it.
def read_user_choice ():
    """ This function prompts the user to enter an integer between 0 and 4 and 
        validates the input to ensure it falls within this range. It returns the integer in string form. """
    try:
        choice = int(input("Enter your choice (0..4): "))
        if choice not in (list(range(0, 5))):
            raise ValueError
    except ValueError:
        print ("Please enter a number 0..4")
        read_user_choice ()   
    else:
        print(f'You entered {choice}.')
        return str (choice)


# Function to check the server 
def check_server (server_address, port_number, database, cid=None):
    """ 
    This function verifies if the server is responsive. If the server responds, it returns True 
    along with the JSON data from the database. It accepts the following arguments:
        server_address
        port_number
        database
        cid
    If a cid is provided, the function checks whether a car with the specified cid exists in 
    the database and returns a boolean result accordingly.
         """
    def is_server_running ():
        try: 
            reply = requests.get(f"{server_address}:{port_number}/{database}")
        except requests.exceptions.InvalidURL:
            print('The URL is invalid.')
            return False, None
        except requests.exceptions.HTTPError:
            print("Bad requests made.")
            return False, None
        except requests.exceptions.Timeout:
            print ("Connection taking longer than expected.")
            return False, None
        except:
            print("Error")
            return False, None
        else:
            if reply.status_code == requests.codes.ok:
                return True, reply.json()
    
    server_running, vehicle_data = is_server_running ()
                

    if server_running and cid is not None:
        print ("Server is running and cid is provided")

        # Check if the cid is present in the database
        if any(vehicle.get("id") == cid for vehicle in vehicle_data):
            print (f'The cid {cid} is in the database.')
            return True, vehicle_data
        else:
            print (f'The cid {cid} is not in the database.')
            return False, None
    elif server_running:
        print ()
        print ("Server is running.")
        return server_running, vehicle_data
    else:
        return False, None
        



# Function to print carlist header.
def print_header ():
    """ 
    Prints the header row for the car list table. 
    
    The header displays column names ('id', 'brand', 'model', 'production_year', 'convertible') 
    aligned according to the specified widths for each column, providing a formatted table header. 
    """
    header_names = ['id', 'brand', 'model', 'production_year', 'convertible']
    widths = [10, 20, 20, 15, 10]
    for n, w in zip(header_names, widths):
        print (n.ljust(w), end = "| ")
    print ()
    print("__"*45)

def print_content (json):
    """ 
    Prints the content of a single car record from JSON data.

    Parameters:
    - json (dict): A dictionary containing car details where keys are expected to be 'id', 
                   'brand', 'model', 'production_year', and 'convertible'.
    
    The function aligns each field according to predefined column widths, printing 
    the row in a table-like format.
    """
    header_names = ['id', 'brand', 'model', 'production_year', 'convertible']
    widths = [10, 20, 20, 15, 10]
    for n, w in zip(header_names, widths):
        print(str(json[n]).ljust(w), end = "| ")
    print ()

def print_json (elements):
    """ 
    Prints the car list in a formatted table view by invoking `print_header` 
    and `print_content` functions. 

    Parameters:
    - elements (list or dict): The JSON data containing car records. If `elements` 
                               is a list, it prints each car record in the list. 
                               If `elements` is a dictionary, it prints a single record.
    
    The function first prints the header, then iterates through each element 
    to display individual car details.
    """
    print_header()
    if type(elements) is list:
        for element in elements:
            print_content(element)
    elif type(elements) is dict:
        if elements:
            print_content(elements)


# function to print list car.
def list_cars (vehicle_data):
    """
    Prints a list of cars from the provided vehicle data. 

    This function checks if there is any data in the vehicle_data parameter. 
    If the data is empty, it prints a message indicating that the database is empty. 
    Otherwise, it calls the `print_json` function to display the car details.

    Parameters:
    vehicle_data (list): A list of dictionaries, where each dictionary contains information about a car.

    Returns:
    None
    """
    size = len([vehicle for vehicle in vehicle_data])
    if size == 0:
        print ("*** Database is empty ***") 
    else:
        print_json(vehicle_data)




# Function to enter and validate Car ID.
def enter_id ():
    """
    Prompts the user to enter a Car ID, validates the input, and returns it.

    This function repeatedly prompts the user to enter a Car ID, which must be a digit-only string.
    If the user enters an empty string, the function returns None and asks again to enter the car id. 
    If the input contains non-digit characters, a ValueError is raised, and an error message is displayed.
    The function returns the valid Car ID as a string when entered correctly.

    Returns:
    str of integer number. The valid Car ID as a string if entered correctly.
    """
    while True:
        try:
            cid = input("enter a Car ID (only integers number are allowed): ")
            if cid == "":
                return None
            if not cid.isdigit():
                raise ValueError
        except ValueError:
            print ("The Car Id must contain only digits.")
        else:
            return cid
           

# Function to validate the car name (brand or model).
def name_is_valid (name):
    """
    Validates the car name (brand or model) to ensure it contains only alphanumeric characters or spaces.

    This function checks that the provided car name is not empty and contains only alphanumeric characters
    and spaces. It returns True if these conditions are met, indicating a valid car name, and False otherwise.

    Parameters:
    name (str): The car name (brand or model) to be validated.

    Returns:
    bool: True if the name is valid (non-empty and contains only alphanumeric characters or spaces),
          False otherwise.
    """
    return bool(name) and all(char.isalnum() or char.isspace() for char in name)


# Function to allow user to enter car brand name and model and checks it's valid.
def enter_name (what):
    """
    Prompts the user to enter a valid car name (brand or model) and validates it.

    Continuously requests a car name (specified by `what`), ensuring it contains only letters, 
    spaces, and digits. The function keeps asking for input until a valid name is entered.

    Parameters:
    what (str): Specifies the type of name being requested, such as "brand" or "model".

    Returns:
    str: The validated car name.
    """
    while True:
        try:
            what= input(f"Enter a Car {what}: ")
            if not name_is_valid (what):
                raise ValueError
        except ValueError:
            print (f"Car brand or model must not be empty string and it should only contain letters, space and digits.")
        else:
            return what

# Function to enter and validate production year.
def enter_production_year ():
    """
    Prompts the user to enter a valid car production year and validates it.

    Continuously asks the user for the car's production year, ensuring it is a four-digit integer 
    between 1900 and 2000. The function keeps requesting input until a valid year is provided.

    Returns:
    int: The validated car production year.
    """
    while True:
        try:
            production_year = input("Car production year: ")
            if production_year == "" or len(production_year) != 4 or not production_year.isdigit():
                raise ValueError
            production_year = int(production_year)
            if not (1900 <= production_year <= 2000):
                raise ValueError


        except ValueError:
            print ("Year must be fourdigit integer value from 1900 to 2000")
        else:
            return production_year


def enter_convertible ():
    """
    Prompts the user to specify if the car is convertible and validates the input.

    Continuously asks the user whether the car is convertible, expecting either 'y' or 'n'.
    If the input is valid, the function returns `True` for convertible cars, `False` for non-convertible cars,
    or `None` if the input is left empty.

    Returns:
    bool or None: `True` if the car is convertible, `False` if not, or `None` if the input is empty.
    """
    while True:
        try:
            convertible = input("Is this car convertible > [y/n] : ")
            if convertible  == "":
                return None
            if (convertible == "y") or (convertible == "Y"):
                return True
            elif (convertible == "n") or (convertible == "N"):
                return False
            else:
                raise ValueError
        except ValueError:
            print ("Enter True if the car is convertible, False otherwise.")
        else:
            return convertible


def input_car_data (with_id):
    """
    Prompts the user to input car data and returns it as a dictionary.

    This function collects the details of a car, including its ID (if `with_id` is `True`),
    brand, model, production year, and whether it is convertible. It validates the input
    for each field and returns the data as a dictionary.

    Parameters:
    with_id (bool): If `True`, the function prompts the user for a car ID; otherwise, it skips this step.

    Returns:
    dict: A dictionary containing the car's details, such as 'id', 'brand', 'model', 'production_year', and 'convertible'.

    Raises:
    ValueError: If `with_id` is not a boolean value (True/False).
    """
    try:
        new_car = {}
        if with_id not in [True, False]:
            raise ValueError
        else:
            if with_id:
                # Add car id if with_id is true.
                cid = enter_id ()
                new_car["id"] = cid
            # This code will excecute regarddless of with_id value.
            brand = enter_name ("brand")
            new_car["brand"] = brand
            # Add a model.
            model = enter_name("model")
            new_car["model"] = model
            # Add production year
            production_year = enter_production_year ()
            new_car["production_year"] = production_year
            # Add convertible
            convertible = enter_convertible()
            new_car["convertible"] = convertible

        # Return the dictionary of the user entered value.
        return new_car
    except ValueError:
        print ("Only True / False is allowed as an argument.")

def add_car (server_address, port_number, database):
    """
    Collects car data from the user and sends it as a POST request to the specified server and database.

    This function prompts the user to input car details (such as ID, brand, model, production year, and convertible status)
    and then sends this data to the server via a POST request to the specified database. If the server responds with a
    successful status, it confirms that the car entry has been added to the database.

    Parameters:
    server_address (str): The address of the server.
    port_number (int): The port number to use for the connection.
    database (str): The name of the database where the car data will be added.

    Returns:
    None

    Exceptions:
    requests.RequestException: If there is a communication error while sending the POST request.
    """
    # Invokes the gathered data.
    data = input_car_data (True)
    # Add the gathered data into the database.
    # Prepare to write a new car data into the database.
    h_close = {"Connection" : "Close"}
    h_content = {"Content-Type" : "application/json"}
    try:
        reply = requests.post(f"{server_address}:{port_number}/{database}", headers=h_content, data = json.dumps(data))
        print (reply.status_code)
    except requests.RequestException:
        print ("Communication error!")
    else:
        if reply.status_code == requests.codes.created:
            print (f'The entry {json.dumps(data)} has been posted to the vehicle database.')
        else:
            print ("Server error!")

def delete_car (server_address, port_number, database):
    """
    Prompts the user for a car ID and attempts to delete the corresponding car entry from the database.

    This function asks the user for the car's ID, validates the input, and sends a DELETE request to the 
    specified server to remove the car entry from the database. If the car is successfully deleted, a 
    success message is displayed. If no entry is found or if there's a communication error, an appropriate message is shown.

    Parameters:
    server_address (str): The address of the server.
    port_number (int): The port number to use for the connection.
    database (str): The name of the database from which the car entry will be deleted.

    Returns:
    None

    Exceptions:
    requests.RequestException: If there is a communication error while sending the DELETE request.
    """
    # Take the car id from the user and validate the cid.
    cid = enter_id ()
    # Delete the car data from the vehicle database with user entered cid.
    headers = {"Connection" : "Close"}
    try:
        reply = requests.delete(f"{server_address}:{port_number}/{database}/{cid}")
        print ("res = " +str(reply.status_code))
    except requests.RequestException:
        print ("Communication error!")
    else:
        if reply.status_code == requests.codes.ok:
            print (f'The entry of {cid} has been deleted successfully from the database.')
        elif reply.status_code == requests.codes.no_content:
            print (f'No entry found with the id of {cid}.')
        else:
            print ("Server error.")

def update_car (server_address, port_number, database):
    """
    Prompts the user for a car ID and updates the corresponding car entry in the database.

    This function asks the user for the car ID (cid), validates it, and then prompts for the updated car data 
    (brand, model, production year, and convertible status). It sends a PUT request to the server to update 
    the car entry in the database. If the update is successful, a confirmation message is shown; if the 
    car ID is not found or if there's a communication error, an appropriate message is displayed.

    Parameters:
    server_address (str): The address of the server.
    port_number (int): The port number to use for the connection.
    database (str): The name of the database where the car data will be updated.

    Returns:
    None

    Exceptions:
    requests.RequestException: If there is a communication error while sending the PUT request.
    """
    cid = str(enter_id ())
    data_to_update = input_car_data (False)
    print (data_to_update)
  
    # Updading the database with new data of the cid.
    h_content = {"Content-Type" : "application/json"}
    try:
        reply = requests.put(f"{server_address}:{port_number}/{database}/{cid}", headers=h_content, data = json.dumps(data_to_update))
        print ("res = " +str(reply.status_code)) 
    except requests.RequestException:
        print ("Comminication error!")
    else:
        if reply.status_code == requests.codes.ok:
            print (f'The new data {data_to_update} has been updated in the entry with cid no. {cid}')
        elif reply.status_code == requests.codes.not_found:
            print (f'The cid no. {cid} is not in the database.')
        else:
            print ("Server error!")




