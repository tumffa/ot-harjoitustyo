class Variable:
    def __init__(self, name, value, string):
        self.name = name
        self.value = value
        self.string = string

    def __str__(self):
        return f"{self.name} = {self.value}"
