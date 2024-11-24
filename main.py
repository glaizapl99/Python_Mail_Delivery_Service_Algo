# Name: Glaiza Lopez
# Student ID: 010956920
import csv
from datetime import datetime, timedelta

from CreateHashMap import CreateHashMap  # import hashmap
from package import Package  # import package class
from truck import Truck  # import truck class


#read address csv
with open("CSV Files/Address_File.csv") as csv_file:
    CSV_Addresses = csv.reader(csv_file)
    CSV_Addresses = list(CSV_Addresses)

#read distance csv
with open ("CSV Files/Distance_File.csv") as csv_file1:
    CSV_Distances = csv.reader(csv_file1)
    CSV_Distances = list(CSV_Distances)

#read package csv
with open ("CSV Files/Package_File.csv") as csv_file2:
    CSV_Packages = csv.reader(csv_file2)
    CSV_Packages = list(CSV_Packages)


#load packages to hash map
def load_packages (filename, package_hash_map):
    with open(filename) as package_info:
        package_data = csv.reader(package_info)
        for package in package_data:
            package_id = int(package[0])
            package_address = package[1]
            package_city = package[2]
            package_state = package[3]
            package_zip = package[4]
            package_deadline = package[5]
            package_weight = package[6]
            package_status = "At Hub"


            #package object
            p = Package(package_id, package_address, package_city, package_state, package_zip, package_deadline, package_weight, package_status)

            #insert into hash map
            package_hash_map.insert(package_id, p)


#find distance between two addresses
def distances_between (x_values, y_values):
    distance = CSV_Distances[x_values][y_values]
    if distance == '':
        distance = CSV_Distances[y_values][x_values]

    return float(distance)

#get address method
def get_address(address):
    for row in CSV_Addresses:
        if address in row[2]:
            return int(row[0])



#instantiate trucks
#truck 1
truck_1 = Truck(16, 18, None, [1, 13, 14, 15, 16, 20, 29, 30, 31, 34, 37, 40], 0.0, "4001 South 700 East", timedelta(hours = 8))

#truck 2
truck_2 = Truck(16, 18, None, [3, 6, 12, 17, 18, 19, 21, 22, 23, 24, 26, 27, 35, 36, 38, 39], 0.0,
                     "4001 South 700 East", timedelta(hours = 10, minutes = 20))

#truck 3
truck_3 = Truck(16, 18, None, [2, 4, 5, 6, 7, 8, 9, 10, 11, 25, 28, 32, 33], 0.0, "4001 South 700 East",
                     timedelta(hours = 9, minutes = 5))

#create hash table
package_hash_map = CreateHashMap()

#load packages to hash table
load_packages("CSV Files/Package_File.csv", package_hash_map)


#helper function to find the nearest package
def find_nearest_package(truck, undelivered_packages):
    nearest_package = None
    shortest_distance = float('inf')  #start with a very large distance

    for package in undelivered_packages:
        distance = distances_between(get_address(truck.address), get_address(package.address))
        if distance < shortest_distance:
            shortest_distance = distance
            nearest_package = package

    return nearest_package, shortest_distance


#deliver packages method
def deliver_packages(truck, truck_number):
    #create a list of undelivered packages
    undelivered_packages = [package_hash_map.lookup(package_id) for package_id in truck.packages]

    #clear the truck's package list to reorder them
    truck.packages.clear()

    #while there are still packages to deliver
    while undelivered_packages:
        #find the nearest package and its distance
        next_package, next_address = find_nearest_package(truck, undelivered_packages)

        if next_package:
            #check if the package is Package 9 and change its address (after 10:20 AM)
            if next_package.package_id == 9 and truck.time >= timedelta(hours=10, minutes=20):
                next_package.address = "410 S State St"  #new address
                next_package.zipcode = "84111" #new zip code

            #load the package onto the truck
            truck.packages.append(next_package.package_id)
            #remove it from the undelivered list
            undelivered_packages.remove(next_package)
            #update truck mileage, address, and time
            truck.mileage += next_address
            truck.address = next_package.address
            truck.time += timedelta(hours=next_address / 18)  # Assuming speed is 18 mph

            #update package delivery details
            next_package.delivery_time = truck.time
            next_package.departure_time = truck.depart_time
            next_package.truck_number = truck_number #set truck number


#load truck 1 and 2
deliver_packages(truck_1, 1)
deliver_packages(truck_2, 2)
#wait till other trucks leave and are finished with loads then truck 3 can go
truck_3.depart_time = min(truck_1.time, truck_2.time)
deliver_packages(truck_3, 3)

def main():
    #ui
    #when program runs, the message below will appear
    print("Welcome to the Western Governors University Parcel Service (WGUPS)!")
    print("The total mileage of the route is:")
    #print total mileage for all trucks
    print(truck_1.mileage + truck_2.mileage + truck_3.mileage)

    #asking for user input to begin the program and anything else will cause the program to quit
    text = input("To begin, please type the word 'begin'"
                 "\n(All else will cause the program to quit)."
                 "\n")

    #if user types 'begin' they will be prompted to enter a time for what package they are searching for
    if text == 'begin':
        try:
            user_begin = input("To check status of package(s), please enter a time using the following format: HH:MM:SS "
                               "\n")
            (h, m, s) = user_begin.split(":")
            current_time = timedelta(hours = int(h), minutes = int(m), seconds = int(s))
            #the user will be prompted to choose between looking at a specific package status or all package statuses
            input_2 = input("To see the status of a specific package, please type the word 'specific'."
                            "\nTo see the status of all packages, please type 'all'."
                            "\n(All else will cause the program to quit)"
                            "\n")
            if input_2 == 'specific':
                try:
                    #the user will be prompted to enter a package ID for the package status they are looking for
                    input_2 = input("Enter the package ID of the package status you would like to see: ")
                    package = package_hash_map.lookup(int(input_2))
                    package.update_status(current_time)
                    print(str(package))
                    print(f"Truck Number: {package.truck_number}")
                except ValueError:
                    print("Invalid entry. The program will now quit. Goodbye!")
                    exit()

            #if user types 'all' all status information of packages will show
            elif input_2 == 'all':
                try:
                    for package_id in range (1, 41):
                        package = package_hash_map.lookup(package_id)
                        package.update_status(current_time)
                        print(str(package))
                        print(f"Truck Number: {package.truck_number}")
                except ValueError:
                    print("Invalid entry. The program will now quit. Goodbye!")
                    exit()
            else:
                exit()
        except ValueError:
            print("Invalid entry. The program will now quit. Goodbye!")
            exit()
    elif input != 'begin':
        print("Invalid entry. The program will now quit. Goodbye!")
        exit()

if __name__ == "__main__":
    main()
