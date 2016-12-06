class JsonObject:
    def __init__(self, id, data):
        self.id = id
        self.data = data

    def __str__(self):
        return "json id: " + str(self.id) + " json data: " + str(self.data)
