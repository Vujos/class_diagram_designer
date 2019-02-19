class ItemFunction():
    def __init__(self, access_modifiers, static, returnType, name, params):
        self.access_modifiers = access_modifiers
        self.static = static
        self.returnType = returnType
        self.name = name
        self.params = params

    def __str__(self):
        return "{} {}{} {} ({})".format(self.access_modifiers, "static " if self.static else "", self.returnType, self.name, ','.join("{} {}".format(k, v) for k, v in self.params.items()))
