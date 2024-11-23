import auxiliares as aux

def main():
    while True:
        print("\n----# Car Sale System #----")
        print("(1) Update inventory")
        print("(2) Check availability")
        print("(3) Get all available cars")
        print("(4) Remove car from inventory")
        print("(0) Exit")
        choice = input("Enter choice: ")

        if choice == '1':
            generate_random = input("(1) Generate random car (2) Enter car manually (3) Use file: ")
            if generate_random == '1':
                aux.update_inventory(generate_random=True, use_file=False)
            elif generate_random == '2':
                aux.update_inventory(generate_random=False, use_file=False)
            elif generate_random == '3':
                aux.update_inventory(generate_random=False, use_file=True)
        elif choice == '2':
            car_model = input("Enter car model: ")
            car_year = input("Enter car year: ")

            aux.check_availability(car_model, car_year)
        elif choice == '3':
            aux.get_all_available_cars()
        elif choice == '4':
            car_id = str(input("Enter car ID: "))
            aux.remove_car_from_inventory(car_id)
        elif choice == '0':
            break
        else:
            print("Invalid choice")

if __name__ == '__main__':
    main()
