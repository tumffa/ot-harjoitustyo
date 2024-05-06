from entities.variable import Variable


class VariableRepository:
    """Class to store and manage variables

    Attributes:
        commands: list of commands used in console
        variables: dictionary of stored variable objects
    """

    def __init__(self, commands=None):
        """Initializes the repository with the given parameters"""
        if commands is None:
            commands = []
        self.commands = commands
        self.variables = {
            'e': Variable('e', 'math.e', 'math.e'),
            'pi': Variable('pi', 'math.pi', 'math.pi')
        }

    def add_variable(self, name, value, string):
        """Adds a variable to the repository

        Args:
            name: the name of the variable
            value: the value of the variable
            string: user input for the variable
        """
        self.variables[name] = Variable(name, value, string)

    def check_identifier(self, name):
        """Checks if the identifier is valid and not already in use

        Args:
            name: the identifier to check

        Returns:
            tuple: (bool, str) where bool is True if the name is valid and not in use
        """
        taken_names = [self.variables, self.commands]
        if not name.isidentifier():
            return (False, "Invalid variable name. Enter name like 'var'\n")
        if any(name in taken for taken in taken_names):
            return (False, "This name is already in use. Enter a new name\n")
        return (True, "")

    def get_variables(self):
        """Returns a dictionary of name : value pairs of the stored variables"""

        return {v.name : v.value for v in self.variables.values()}
