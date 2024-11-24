class Package:
    def __init__(self, package_id, address, city, state, zipcode, deadline, weight, status):
        self.package_id = package_id
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.deadline = deadline
        self.weight = weight
        self.status = status
        self.truck_number = None
        self.delivery_time = None
        self.departure_time = None
        self.correction_time = None #time when address is corrected
        self.corrected_address = None #corrected address

    def __str__(self):
        return "%s, %s, %s, %s, %s, %s, %s, %s, %s" % (self.package_id, self.address, self.city, self.state, self.zipcode, self.deadline, self.weight, self.status, self.delivery_time)

    def update_status(self, current_time):
        if self.delivery_time < current_time:
            self.status = "Delivered"
        elif self.departure_time > current_time:
            self.status = "In Transit"
        else:
            self.status = "At Hub"

    def get_current_address(self, current_time):
        if self.correction_time and current_time >= self.correction_time:
            return self.corrected_address #return corrected address
        return self.address #return initial address
