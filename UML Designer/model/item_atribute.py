class ItemAtribute():
    def __init__(self, access_modifiers, name, atribute_type):
        self.access_modifiers = access_modifiers
        self.name = name
        self.atribute_type = atribute_type

    def __str__(self):
        return "{} {} : {}".format(self.access_modifiers, self.name, self.atribute_type)

    def __repr__(self):
        return "{},{},{}|".format(self.access_modifiers, self.name, self.atribute_type)
