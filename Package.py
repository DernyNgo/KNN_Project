# Create a Package class to hold packages
class Package:
    # Space & Time complexities: O(1) for all
    def __init__(self, id, address, city, state, zipcode, deadline, weight, status):
        self.id = id
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.deadline = deadline
        self.weight = weight
        # Add a status portion to display and track the status of each package
        self.status = status
        self.initial_time = None
        self.in_transit = None
        self.delivered = False

    def __str__(self):
        return "%s, %s, %s, %s, %s, %s, %s, %s, Time for Delivery: %s" % (self.id, self.address, self.city, self.state,
                                                                          self.zipcode, self.deadline, self.weight,
                                                                          self.status, self.in_transit)

    # Updates package status based on comparing truck departure time, and user inputted time
    # Space & Time complexities: O(1)
    def update_package_status(self, time_right_now):
        if time_right_now >= self.in_transit:
            self.status = "Delivered"
        elif time_right_now < self.initial_time:
            self.status = "At the Hub"
        else:
            self.status = "Currently in transit"
