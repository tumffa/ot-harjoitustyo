class Variable:
    """Class to store information about a variable

    Attributes:
        name: the name of the variable
        value: the value of the variable
        string: user input for the variable
    """

    def __init__(self, name, value, string):
        """Initializes the variable with the given parameters"""

        self.name = name
        self.value = value
        self.string = string

    def __str__(self):
        return f"{self.name} = {self.value}"
