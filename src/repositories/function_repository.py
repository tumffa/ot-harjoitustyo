from entities.function import Function


class FunctionRepository:
    """Class to store and manage functions

    Attributes:
        commands: list of commands used in console
        functions: dictionary of stored function objects
    """

    def __init__(self, commands=None):
        """Initializes the repository with the given parameters"""

        if commands is None:
            commands = []
        self.commands = commands
        self.functions = {
            'abs': Function('abs', 'abs', 'abs(x)', eval("lambda x: abs(x)")), # pylint: disable=eval-used
            'sqrt': Function('sqrt', 'math.sqrt', 'math.sqrt(x)', eval("lambda x: sqrt(x)")), # pylint: disable=eval-used
            'exp': Function('exp', 'math.exp', 'math.exp(x)', eval("lambda x: exp(x)")), # pylint: disable=eval-used
            'sin': Function('sin', 'math.sin', 'math.sin(x)', eval("lambda x: sin(x)")), # pylint: disable=eval-used
            'cos': Function('cos', 'math.cos', 'math.cos(x)', eval("lambda x: cos(x)")) # pylint: disable=eval-used
        }

    def add_function(self, function_name, function_string, global_string, result):
        """Adds a function to the repository

        Args:
            function_name: the name of the function
            function_string: the function
            global_string: the global function name
            result: the lambda function to evaluate
        """
        self.functions[function_name] = Function(function_name,
                                                 global_string,
                                                 function_string,
                                                 result)

    def check_identifier(self, name):
        """Checks if the identifier is valid and not already in use

        Args:
            name: the identifier to check

        Returns:
            tuple: (bool, str) where bool is True if the name is valid and not in use
        """

        taken_names = [self.functions, self.commands]
        if not name.isidentifier():
            return (False, "Invalid function name. Enter name like f_1\n")
        if any(name in taken for taken in taken_names):
            return (False, "This name is already in use. Enter a new name\n")
        return (True, "")

    def get_functions(self):
        """Returns a dictionary of name : (global_name, function) pairs of the stored functions"""

        return {f.name : (f.func, f.string) for f in self.functions.values()}
