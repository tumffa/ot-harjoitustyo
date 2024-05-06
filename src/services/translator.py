import math # pylint: disable=unused-import
# math is used when using eval() on strings
import random
import string as s
import sympy as sp
from repositories.function_repository import FunctionRepository
from repositories.variable_repository import VariableRepository

class Translator:
    """This class is used to handle and evaluate mathematical 
        expressions and to store functions and variables

    Attributes:
        function_repository: FunctionRepository object
        variable_repository: VariableRepository object
    """

    def __init__(self, f_repo=None, v_repo=None):
        """Initializes the class with default repositories"""

        if f_repo is None:
            f_repo = FunctionRepository()
        if v_repo is None:
            v_repo = VariableRepository()
        self.f_repo = f_repo
        self.v_repo = v_repo

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
            with the global functions and variable values

        Args:
            string: the expression to check
            keep: a variable to keep in the expression

        Returns:
            string: the expression with functions and variables replaced
            False: if the expression is invalid
        """
        functions = self.f_repo.get_functions()
        variables = self.v_repo.get_variables()
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
                if word in functions:
                    replacement = functions[word][0]
                    increment = len(functions[word][0])
                elif word in variables:
                    replacement = variables[word]
                    increment = len(variables[word])
                else:
                    return False
                string = f"{string[:i]}{replacement}{string[j:]}"
                i += increment
            else:
                i += 1
        return string

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
            check = self.f_repo.check_identifier(function_name)
            if check[0] is False:
                io.write(check[1])
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
            function_string = function_string.replace("^", "**")
            string = self.check_and_replace(function_string, keep=variable)
            if string is False:
                io.write("Invalid identifiers used in function!\n")
                continue
            try:
                result = eval(f'lambda {variable}: {string}') # pylint: disable=eval-used
            except:
                io.write("Invalid expression!\n")
                continue
            random_string = ''.join(random.choices(s.ascii_letters + s.digits, k=10))
            globals()[random_string] = result
            self.f_repo.add_function(function_name, string, random_string, result)
            io.write(f"\nFunction '{function_name}(x)' added successfully!\n")
            return True

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
            check = self.v_repo.check_identifier(variable_name)
            if check[0] is False:
                io.write(check[1])
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
            variable_string = variable_string.replace("^", "**")
            string = self.check_and_replace(variable_string)
            if string is False:
                io.write("Invalid expression!\n")
                continue
            try:
                result = eval(string) # pylint: disable=eval-used
            except:
                io.write("Invalid expression!\n")
                continue
            self.v_repo.add_variable(variable_name, str(result), variable_string)
            io.write(f"\nVariable '{variable_name}' added successfully!\n")
            return True

    def print_functions(self, io):
        funcs = self.f_repo.get_functions()
        io.write("\n")
        for name, value in funcs.items():
            io.write(f"   {name}(x) = {value[1]}")
        io.write("\n")

    def print_variables(self, io):
        variables = self.v_repo.get_variables()
        io.write("\n")
        for name, value in variables.items():
            io.write(f"   {name} = {value}")
        io.write("\n")

    def solve_equation_prompt(self, io):
        """Prompts the user to solve an equation, prints solutions if valid

        Args:
            io: ConsoleIO object

        Returns:
            boolean: True if the equation was solved, False if the user cancels
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
        try:
            sympy_equation = sp.sympify(equation)
        except:
            io.write("Invalid expression. Use only variable x and numbers\n")
            return False
        try:
            solution = sp.solve(sympy_equation, x)
        except:
            io.write("Unable to solve\n")
            return False
        if solution == []:
            io.write("No solution\n")
            return True

        io.write(f"\nSolution: {solution}\n")
        return True
