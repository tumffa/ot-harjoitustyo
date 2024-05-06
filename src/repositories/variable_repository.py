from entities.variable import Variable


class VariableRepository:
    def __init__(self, commands=None):
        if commands is None:
            commands = []
        self.commands = commands
        self.variables = {
            'e': Variable('e', 'math.e', 'math.e'),
            'pi': Variable('pi', 'math.pi', 'math.pi')
        }

    def add_variable(self, name, value, string):
        self.variables[name] = Variable(name, value, string)

    def check_identifier(self, name):
        taken_names = [self.variables, self.commands]
        if not name.isidentifier():
            return (False, "Invalid variable name. Enter name like 'var'\n")
        if any(name in taken for taken in taken_names):
            return (False, "This name is already in use. Enter a new name\n")
        return (True, "")

    def get_variables(self):
        return {v.name : v.value for v in self.variables.values()}
