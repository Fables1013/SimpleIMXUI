

class Proto:
    def __init__(self):
        self.id = None
        self.name = None
        self.effect = None
        self.god = None
        self.rarity = None
        self.tribe = None
        self.mana = None
        self.attack = None
        self.health = None
        self.type = None
        self.set = None
        self.collectable = None
        self.live = None
        self.art_id = None
        self.lib_id = None

    def setFields(self, fieldsDict):
        for k, v in fieldsDict.items():
            setattr(self, k, v)
        return self

    def __eq__(self, other):
        return self.name == other.name

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.name)

    def urlEncode(self):
        return {"proto": str(self.id)}


