

class GodsUnchainedProtoCache:
    def __init__(self, data):
        self.data = data

    def addEntries(self, data):
        if self.data is None:
            self.data = data
        else:
            self.data.update(data)

    def addEntry(self, proto):
        self.data.add(proto)

    def getAllProtos(self):
        return self.data

    def contains(self, proto):
        return proto in self.data

    def fromName(self, name):
        return next(p for p in self.data if p.name == name)


