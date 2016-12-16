class JsonObject:
    def __init__(self, id, data, password):
        self.id = id
        self.data = data
        self.password = password

    def __str__(self):
        return "json id: " + str(self.id) + " json data: " + str(self.data)
