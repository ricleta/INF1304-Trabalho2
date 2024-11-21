import requests
import json
import random as rd

# CHANGE THIS URL TO MATCH YOUR LAMBDA FUNCTION URL
update_inventory_url = "https://6iim4chjw4dp7omphd2xf6tdtm0yspcz.lambda-url.us-east-1.on.aws/"
check_availability_url = "https://cs63kfkves6seapyd74ewg7vcq0swkyu.lambda-url.us-east-1.on.aws/"


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


def update_inventory(generate_random_car = False):
    if generate_random_car:
        car = generate_random_car()
    else:
        car = get_car()
    
    print(f"Updating inventory for {car['name']} {car['year']}...")
    
    dados = json.dumps(car)

    header = {
        'Content-Type': 'application/json',
    }

    response = requests.post(update_inventory_url, data=dados, headers=header)

    print(response.text)

def check_availability(car_model, car_year):
    print(f"Checking availability for {car_model} {car_year}...")

    dados = {
        'car_model': car_model,
        'car_year': car_year
    }

    header = {
        'Content-Type': 'application/json',
    }

    response = requests.post(check_availability_url, data=json.dumps(dados), headers=header)

    print(response.text)
