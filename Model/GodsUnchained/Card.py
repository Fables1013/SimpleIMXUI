from enum import Enum


class Rarity(Enum):
    Legendary = "legendary"
    Epic = "epic"
    Rare = "rare"
    Common = "common"
    Mythic = "mythic"
    All = "all"


class Set(Enum):
    Core = "core"
    Welcome = "welcome"
    Genesis = "genesis"
    Trial = "trial"
    Order = "order"
    Etherbots = "etherbots"
    Promo = "promo"
    Mythic = "mythic"
    All = "all"


class Class(Enum):

    War = "war"
    Nature = "nature"
    Magic = "magic"
    Light = "light"
    Death = "death"
    Deception = "deception"
    Neutral = 'neutral'
    All = "all"


class Quality(Enum):
    Meteorite = "Meteorite"
    Shadow = "Shadow"
    Gold = "Gold"
    Diamond = "Diamond"


class Card:
    def __init__(self, proto, quality=Quality.Meteorite):
        self.proto = proto
        self.quality = quality

    def __eq__(self, other):
        return self.proto.name == other.name and self.quality == other.quality

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((self.proto.name, self.quality))

    def setQuality(self, q):
        self.quality = q

    def withQuality(self, q):
        return Card(self.proto, q)

    def urlEncode(self):
        return ""