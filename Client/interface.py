import auxiliares as aux

def main():
    while True:
        print("(1) Update inventory")
        print("(2) Check availability")
        print("(0) Exit")
        choice = input("Enter choice: ")

        if choice == '1':
            aux.update_inventory()
        elif choice == '2':
            car_model = input("Enter car model: ")
            car_year = input("Enter car year: ")

            aux.check_availability(car_model, car_year)
        elif choice == '0':
            break
        else:
            print("Invalid choice")

if __name__ == '__main__':
    main()
