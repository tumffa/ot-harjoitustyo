import math # pylint: disable=unused-import
# math is used when using eval() on strings
import random
import string as s
import sympy as sp

class Translator:
    """This class is used to handle and evaluate mathematical 
        expressions and to store functions and variables

    Attributes:
        functions: dictionary of functions that can be used in expressions
        variables: dictionary of variables that can be used in expressions
    """

    def __init__(self):
        """Initializes the class with default functions and variables
        """

        # first value is what is evaluated in code
        # second value is user input / what is displayed with print
        self.functions = {
            'abs': ('abs', 'abs(x)'),
            'sqrt': ('math.sqrt', 'math.sqrt(x)'),
            'exp': ('math.exp', 'math.exp(x)'),
            'sin': ('math.sin', 'math.sin(x)'),
            'cos': ('math.cos', 'math.cos(x)')
            }

        self.variables = {
            'e': ('math.e', 'math.e'),
            'pi': ('math.pi', 'math.pi')
        }

    def calculate(self, string):
        """Evaluates a mathematical expression

        Args:
            string: the expression to evaluate

        Returns:
            float/integer: the result of the expression if it is valid, else False
        """

        string = string.replace("^", "**")
        # check for injection
        string = self.check_and_replace(string)
        if string is False:
            return False
        # evaluate result
        try:
            result = eval(string) # pylint: disable=eval-used
            # injection is avoided as only self.functions or user created functions
            # (which are stored as a random 10-char string) are allowed
        except:
            return False
        return result

    def check_and_replace(self, string, keep=None):
        """Checks for injection and replaces functions and variables 
            with the actual functions and variables

        Args:
            string: the expression to check
            keep: a variable to keep in the expression

        Returns:
            string: the expression with functions and variables replaced
            False: if the expression is invalid
        """
        i = 0
        while i < len(string):
            if string[i].isalpha() or string[i] == '_':
                j = i
                while j < len(string) and string[i:j+1].isidentifier():
                    j += 1
                word = string[i:j]
                if word == keep:
                    i = j
                    continue
                if word in self.functions:
                    replacement = self.functions[word][0]
                    increment = len(self.functions[word][0])
                elif word in self.variables:
                    replacement = self.variables[word][0]
                    increment = len(self.variables[word][0])
                else:
                    return False
                string = f"{string[:i]}{replacement}{string[j:]}"
                i += increment
            else:
                i += 1
        return string

    def add_function(self, function_name, function_string, variable):
        """Adds a function to the functions dictionary

        Args:
            function_name: name of the function
            function_string: the expression
            variable: the variable used in the expression

        Returns:
            boolean: True if the function was added, False if the expression is invalid
        """
        function_string = function_string.replace("^", "**")
        # check for injection
        function_string2 = self.check_and_replace(function_string, keep=variable)
        # generate a random string to use as the function name
        random_string = ''.join(random.choices(s.ascii_letters, k=10))
        try:
            # check if the function is valid
            result = eval(f'lambda {variable}: {function_string2}') # pylint: disable=eval-used
        except:
            return False
        # save the actual function with random identifier
        globals()[random_string] = result
        self.functions[function_name] = (random_string, function_string)
        return True

    def add_variable(self, variable_name, variable_string):
        """Adds a variable to the variables dictionary

        Args:
            variable_name: name of the variable
            variable_string: the expression

        Returns:
            boolean: True if the variable was added, False if the expression is invalid
        """

        variable_string = variable_string.replace("^", "**")
        # check for injection
        variable_string2 = self.check_and_replace(variable_string)
        try:
            # check if the variable is valid
            result = eval(variable_string2) # pylint: disable=eval-used
        except:
            return False
        self.variables[variable_name] = (str(result), variable_string)
        return True

    def add_function_prompt(self, io):
        """Prompts the user to add a function

        Args:
            io: ConsoleIO object
        
        Returns:
            boolean: True if the function was added, False if the user cancels
        """

        # prompt for function name
        io.write("\nEnter the name of the function, i.e. 'f_1' -- 'exit' to cancel")
        while True:
            if len(io.inputs) == 0:  # pragma: no cover
                io.add_input("name: ")  # pragma: no cover
            function_name = io.read()
            if function_name == "exit":  # pragma: no cover
                return False  # pragma: no cover
            if not function_name.isidentifier():
                io.write("Invalid function name. Enter name like f_1\n")
                continue
            taken = self.check_available(function_name)
            if taken is False:
                io.write("This name is already in use. Enter a new name\n")
                continue
            break

        # prompt for function
        io.write("\nEnter the function. I.e. 'x**2'")
        while True:
            if len(io.inputs) == 0:  # pragma: no cover
                io.add_input("function: ")  # pragma: no cover
            function_string = io.read()
            if function_string == "exit":  # pragma: no cover
                return False  # pragma: no cover
            variable = 'x'
            if self.check_and_replace(function_string, keep=variable) is False:
                io.write("Invalid function. Use expressions, functions, stored variables or 'x'\n")
                continue
            result = self.add_function(function_name, function_string, variable)
            if result is True:
                io.write(f"\nFunction '{function_name}' added successfully!\n")
                return True
            io.write("Invalid expression\n")

    def add_variable_prompt(self, io):
        """Prompts the user to add a variable

        Args:
            io: ConsoleIO object
        
        Returns:
            boolean: True if the function was added, False if the user cancels
        """

        # prompt for variable name
        io.write("\nEnter the name of the variable: -- 'exit' to cancel")
        while True:
            if len(io.inputs) == 0:  # pragma: no cover
                io.add_input("name: ")
            variable_name = io.read()
            if variable_name == "exit": # pragma: no cover
                return False # pragma: no cover
            if not variable_name.isidentifier():
                io.write("Invalid variable name. Enter name like 'var'\n")
                continue
            taken = self.check_available(variable_name)
            if taken is False:
                io.write("This name is already in use. Enter a new name\n")
                continue
            break

        # prompt for variable
        io.write("\nEnter the variable. I.e. '2 + e^2 + f(5)'")
        while True:
            if len(io.inputs) == 0: # pragma: no cover
                io.add_input("variable: ") # pragma: no cover
            variable_string = io.read()
            if variable_string == "exit":
                return False
            if self.check_and_replace(variable_string) is False:
                io.write("Invalid variable. Use expressions, variables or functions\n")
                continue
            result = self.add_variable(variable_name, variable_string)
            if result is True:
                io.write(f"\nVariable '{variable_name}' added successfully!\n")
                return True
            io.write("Invalid expression\n")

    def print_functions(self, io):
        io.write("\n")
        for name, value in self.functions.items():
            io.write(f"   {name}(x): {value[1]}")
        io.write("\n")

    def print_variables(self, io):
        io.write("\n")
        for name, value in self.variables.items():
            io.write(f"   {name}: {value[1]}")
        io.write("\n")

    def check_available(self, name):
        taken_names = [self.functions, self.variables, ['af', 'av', 'variables', 'functions', 'x']]
        return not any(name in names for names in taken_names)

    def solve_equation_prompt(self, io):
        """Prompts the user to solve an equation

        Args:
            io: ConsoleIO object

        Returns:
            list: list of the solutions to the equation
            False: if the user cancels or the equation is invalid
        """
        io.write("\nEnter the equation to solve. I.e. '2*x + 3 = 0'")
        while True:
            if len(io.inputs) == 0:  # pragma: no cover
                io.add_input("equation: ")  # pragma: no cover
            equation = io.read()
            if equation == "exit":
                return False
            if '=' not in equation:
                io.write("Invalid equation. Use ' = ' to separate the left and right sides\n")
                continue
            break

        equation = equation.replace("^", "**")

        left, right = equation.split('=')
        left = self.check_and_replace(left, keep='x')
        right = self.check_and_replace(right, keep='x')

        if left is False or right is False:
            io.write("Invalid expression. Use only variable x and numbers\n")
            return False
        equation = f"({left}) - ({right})"

        x = sp.symbols('x')
        solution = sp.solve(sp.sympify(equation), x)

        io.write(f"\nSolution: {solution}\n")
        return True
