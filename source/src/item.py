__author__ = 'capgeti'


class Weapon:
    def __init__(self, damage, name, schuss, schusskapa, magazine, abklingzeit, objName):
        self.damage = damage
        self.name = name
        self.schuss = schuss
        self.schusskapa = schusskapa
        self.magazine = magazine
        self.abklingzeit = abklingzeit
        self.objName = objName

class Pistole(Weapon):
    def __init__(self):
        Weapon.__init__(self, 15, "Pistole", 8, 8, 1, 20, "weapon01")


class Mp(Weapon):
    def __init__(self):
        Weapon.__init__(self, 5, "MP", 32, 32, 2, 5, "weapon02")


wrapper = {
    "weapon01": Pistole,
    "weapon02": Mp
    }
