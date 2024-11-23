import requests
import json
import pymysql
import random as rd

# Lambda
update_inventory_url = "https://wtp5licbmz3afmubx6toolaeba0retzw.lambda-url.us-east-1.on.aws/"
add_waiting_user_url = "https://vy4utmnut4kryugy5xrqgj6v7y0uuumz.lambda-url.us-east-1.on.aws/"
check_availability_url = "https://cs63kfkves6seapyd74ewg7vcq0swkyu.lambda-url.us-east-1.on.aws/"

# MySQL
host = 'mtcarsdb.c9qca4k6aw1y.us-east-1.rds.amazonaws.com'
user = "mtcarsUsername"
password = "mtcars123"
database = "MTCars"

def get_car():
    car = {}

    car['name'] = input("Enter car name: ")
    car['mpg'] = float(input("Enter miles per gallon (mpg): "))
    car['cyl'] = int(input("Enter number of cylinders (cyl): "))
    car['disp'] = float(input("Enter displacement (disp): "))
    car['hp'] = int(input("Enter horsepower (hp): "))
    car['wt'] = float(input("Enter weight (wt): "))
    car['qsec'] = float(input("Enter quarter-mile time (qsec): "))
    car['vs'] = int(input("Enter engine type (vs, 0 = V-shaped, 1 = straight): "))
    car['am'] = int(input("Enter transmission type (am, 0 = automatic, 1 = manual): "))
    car['gear'] = int(input("Enter number of forward gears (gear): "))
    car['ano'] = input("Enter year (ano): ")

    return car

def generate_random_car():
    car = {}
    
    car['name'] = rd.choice([
        "Mazda RX4",
        "Mazda RX4 Wag",
        "Datsun 710",
        "Hornet 4 Drive",
        "Hornet Sportabout",
        "Valiant",
        "Duster 360",
        "Merc 240D",
        "Merc 230",
        "Merc 280",
        "Merc 280C",
        "Merc 450SE",
        "Merc 450SL",
        "Merc 450SLC",
        "Cadillac Fleetwood",
        "Lincoln Continental",
        "Chrysler Imperial",
        "Fiat 128",
        "Honda Civic",
        "Toyota Corolla",
        "Toyota Corona",
        "Dodge Challenger",
        "AMC Javelin",
        "Camaro Z28",
        "Pontiac Firebird",
        "Fiat X1-9",
        "Porsche 914-2",
        "Lotus Europa",
        "Ford Pantera L",
        "Ferrari Dino",
        "Maserati Bora",
        "Volvo 142E",
        "Honda HRV"
    ])

    car['mpg'] = float(rd.uniform(10, 40))
    car['cyl'] = int(rd.choice([4, 6, 8]))
    car['disp'] = float(rd.uniform(70, 500))
    car['hp'] = int(rd.randint(50, 400))
    car['wt'] = float(rd.uniform(1, 5))
    car['qsec'] = float(rd.uniform(14, 23))
    car['vs'] = int(rd.choice([0, 1]))
    car['am'] = int(rd.choice([0, 1]))
    car['gear'] = int(rd.choice([3, 4, 5]))

    car['ano'] = str(1990 + rd.randint(0, 30))

    return car


def update_inventory(generate_random = True, use_file = False):
    car = {}
    if generate_random:
        print("Generating random car...")
        car = generate_random_car()
        print(f"Generated car: {car}")
    else:
        if use_file:
            print("Reading car from file...")
            path = "./cars/" + input("Enter file name: ") + ".json"
            with open(path, "r") as file:
                car = json.load(file)
        else:
            car = get_car()
    
    print(f"Updating inventory for {car['name']} {car['ano']}...")
    
    dados = json.dumps({'car': car})

    header = {
        'Content-Type': 'application/json',
    }

    # print(dados)
    response = requests.post(update_inventory_url, data=dados, headers=header)

    print(response.text)

def check_availability(car_model, car_year):
    usr = input("Enter your email: ")
    print(f"Checking availability for {car_model} {car_year}...")

    dados = {
        'email': str(usr),
        'car_model': car_model,
        'car_year': car_year
    }

    header = {
        'Content-Type': 'application/json',
    }

    response = requests.post(check_availability_url, data=json.dumps(dados), headers=header)

    if response.status_code == 200:
        print(response.text)
    elif response.status_code == 404:
        print(response.text)
        ans = input("Do you want to be added to the waiting list? (y/n) ")
        if ans.lower() == 'y':
            add_waiting_user(usr, car_model, car_year)
        else:
            print("Ok, see you later!")
    elif response.status_code == 400:
        print(response.text)
    elif response.status_code == 500:
        print(response.text)
    
    # print(response.text)

def add_waiting_user(email, car_name, car_year):
    print(f"Adding {email} to the waiting list for {car_name} {car_year}...")

    dados = {
        "email": email,
        "car_name": car_name,
        "car_year": car_year
    }

    header = {
        'Content-Type': 'application/json',
    }

    response = requests.post(add_waiting_user_url, data=json.dumps(dados), headers=header)

    print(response.text)

def get_all_available_cars():
    print("Getting all available cars...")
    print("---------##--------")

    mysql_config = {
        'host': host,
        'user': user,
        'password': password,
        'database': database
    }

    try:
        connection = pymysql.connect(**mysql_config)
        cursor = connection.cursor()
    except pymysql.MySQLError as e:
        print(f"Error connecting to MySQL Platform: {e}")
        return

    try:
        cursor.execute("SELECT * FROM MTCars")
    except pymysql.MySQLError as e:
        print(f"Error executing query: {e}")
        return
    
    registers = cursor.fetchall()

    print("ID | Name | MPG | Cyl | Disp | HP | WT | Qsec | VS | AM | Gear | Ano")
    for register in registers:
        print(register)

    print("---------##--------")

    cursor.close()
    connection.close()

def remove_car_from_inventory(car_id):
    print("---------##--------")

    mysql_config = {
        'host': host,
        'user': user,
        'password': password,
        'database': database
    }

    try:
        connection = pymysql.connect(**mysql_config)
        cursor = connection.cursor()
    except pymysql.MySQLError as e:
        print(f"Error connecting to MySQL Platform: {e}")
        return

    try:
        cursor.execute(f"SELECT * FROM MTCars WHERE ID = {car_id}")
        car = cursor.fetchone()
    except pymysql.MySQLError as e:
        print(f"Error executing query: {e}")
        return
    
    if car is None:
        print(f"Car with ID {car_id} not found in inventory")
        return
    
    print("ID | Name | MPG | Cyl | Disp | HP | WT | Qsec | VS | AM | Gear | Ano")
    decision = input(f"{car}\nAre you sure you want to remove the this car from the inventory? (y/n)\n")

    if decision.lower() != 'y':
        print("Ok, see you later!")
        return
    
    print(f"Removing car with ID {car_id} from inventory...")
    
    try:
        cursor.execute(f"DELETE FROM MTCars WHERE ID = {car_id}")
        connection.commit()
    except pymysql.MySQLError as e:
        print(f"Error executing query: {e}")
        return
    
    print("Car removed successfully!")
    print("---------##--------")

    cursor.close()
    connection.close()