# Create Truck class
class Truck:
    # Space & Time complexities: O(1) for all
    def __init__(self, capacity, speed, load, packages, address, departure):
        self.capacity = capacity
        self.speed = speed
        self.load = load
        self.packages = packages
        self.address = address
        self.departure = departure
        self.time = departure
        self.mileage = 0

    def __str__(self):
        return "%s, %s, %s, %s, %s, %s, %s" % (self.capacity, self.speed, self.load, self.packages, self.mileage,
                                               self.address, self.departure)

