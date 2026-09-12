class Road:
    def __init__(self, location, owner_id):
        self.location = location
        self.owner_id = owner_id
        self.type = "road"

class Settlement:
    def __init__(self, location, owner_id):
        self.location = location
        self.owner_id = owner_id
        self.type = "settlement"

class City:
    def __init__(self, location, owner_id):
        self.location = location
        self.owner_id = owner_id
        self.type = "city"
