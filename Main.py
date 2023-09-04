#Daniel Ngo

# Overall time complexity: O(n^2)
# Overall space complexity: O(n)

import csv
import datetime
from Hashtable import HashTable
from Package import Package
from Truck import Truck

# Set hash table to be callable
package_hash_table = HashTable()

# Read and store data from "Packages.csv" file
with open("Packages.csv") as package_data:
    initiate_package_data = csv.reader(package_data)
    initiate_package_data = list(initiate_package_data)

# Read and store data from "Distances.csv" file
with open("Distances.csv") as distance_data:
    initiate_distance_data = csv.reader(distance_data)
    initiate_distance_data = list(initiate_distance_data)

# Read and store data from "Addresses.csv" file
with open("Addresses.csv") as address_data:
    initiate_address_data = csv.reader(address_data)
    initiate_address_data = list(initiate_address_data)


# Create packages using csv data, store in a list
# Space & Time complexities: O(n)
def load_package_data(filename):
    with open(filename) as package_contents:
        open_package_data = csv.reader(package_contents)
        # Add parameters to package object
        for package in open_package_data:
            id = package[0]
            address = package[1]
            city = package[2]
            state = package[3]
            zipcode = package[4]
            deadline = package[5]
            weight = package[6]
            status = "At the Hub"

            # Create package object
            package_object = Package(id, address, city, state, zipcode, deadline, weight, status)

            # Insert data into hash table
            package_hash_table.insert(id, package_object)


# Load package data
load_package_data("Packages.csv")


# Find differences in distance from distance data in csv file
# Space & Time complexities: O(n)
def differences_in_distances(address1, address2):
    distance = initiate_distance_data[address1][address2]
    if distance == '':
        distance = initiate_distance_data[address2][address1]
    return float(distance)


# Load addresses from address data in csv file
# Space & Time complexities: O(n)
def address_index(address):
    for row in initiate_address_data:
        if address in row[2]:
            return int(row[0])


# Manually load the Trucks with packages
# Assign trucks packages based on manually sorting by notes and deadlines
truck_one_packages = [1, 5, 13, 14, 15, 16, 19, 20, 29, 30, 31, 34, 37, 40]
truck_two_packages = [3, 6, 18, 25, 28, 32, 35, 36, 38, 39]
truck_three_packages = [2, 4, 7, 8, 9, 10, 11, 12, 17, 21, 22, 23, 24, 26, 27, 33]

# Create truck objects and add parameters accordingly
# Space & Time complexity: O(1) (constant)
truck1 = Truck(16, 18, None, truck_one_packages, '4001 South 700 East', datetime.timedelta(hours=8))
truck2 = Truck(16, 18, None, truck_two_packages, '4001 South 700 East', datetime.timedelta(hours=9, minutes=30))
truck3 = Truck(16, 18, None, truck_three_packages, '4001 South 700 East', datetime.timedelta(hours=10, minutes=20))

# Group trucks in variable for ease of access in package delivery code
trucks = [truck1, truck2, truck3]


# Create function to deliver packages: Nearest Neighbor Algorithm
# Time complexity: O(n^2) (non-linear) Space complexity: O(n) (linear)
def package_delivery():
    for truck in trucks:
        # Create an empty list to store packages
        unsorted_list = []
        # Collect packages for the current truck
        for package_id in truck.packages:
            package = package_hash_table.search(str(package_id))
            # Add the package to the unsorted list
            unsorted_list.append(package)
            # Clear the packages from the truck
        truck.packages.clear()
        while len(unsorted_list) > 0:
            # Set an initial (large) distance
            distance_next = 1000
            # Initialize the next package as None
            next_package = None
            # Find the next package with the shortest distance
            for package in unsorted_list:
                if differences_in_distances(address_index(truck.address),
                                            address_index(package.address)) <= distance_next:
                    # Set the current package as the next package
                    next_package = package
                    distance_next = differences_in_distances(address_index(truck.address),
                                                             address_index(package.address))
            # Add the next package to the truck
            truck.packages.append(next_package.id)
            # Remove the next package from the unsorted list
            unsorted_list.remove(next_package)
            # Update the truck's delivery time
            truck.time += datetime.timedelta(hours=distance_next / 18)
            # Update the truck's current address
            truck.address = next_package.address
            # Update the truck's mileage
            truck.mileage += distance_next
            # Update the package's in-transit time
            next_package.in_transit = truck.time
            next_package.initial_time = truck.departure


# Call the package delivery function
package_delivery()


# Create the menu option for users (CLI)
# Time & Space complexities: O(n)
class Main:
    # Introduction line
    print("\nWestern Governors University Parcel Service\n")
    # Present users with 3 options
    print("Please choose one of the following menu options:\n1. View all packages' status\n"
          "2. View the status of a certain package\n3. Exit out of this menu")
    options_input = input("Enter 1, 2, or 3: ")
    # Enter the time to see all package statuses
    # Print total mileage for all packages
    if options_input == "1":
        # Collect user input, format input
        time_input = input("Please enter the current time. Use the format HH:MM:SS: ")
        (hours, minutes, seconds) = time_input.split(":")
        timedelta = datetime.timedelta(hours=int(hours), minutes=int(minutes), seconds=int(seconds))
        # Print the total sum of truck mileage
        print("Total Mileage: " + str(truck1.mileage + truck2.mileage + truck3.mileage))
        # Loop through package parameters
        for package_id in range(1, 41):
            package = package_hash_table.search(str(package_id))
            package.update_package_status(timedelta)
            # Print packages and parameters
            print(str(package))
    # Enter the time and specific package ID to see package status
    elif options_input == "2":
        time_input = input("Please enter the current time. Use the format HH:MM:SS: ")
        (hours, minutes, seconds) = time_input.split(":")
        timedelta = datetime.timedelta(hours=int(hours), minutes=int(minutes), seconds=int(seconds))
        package_input = input("Enter the package ID: ")
        package = package_hash_table.search(package_input)
        package.update_package_status(timedelta)
        print(str(package))
    # Exit the menu
    elif options_input == '3':
        print("Thank you for using WGU's Parcel Service! Have a great day.")
