import math
import random
import string as s

class Translator:
    def __init__(self):
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
        # check for injection and replace given functions with actual functions
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
                type = None
                if word in self.functions:
                    type = 'function'
                elif word in self.variables:
                    type = 'variable'
                if type is None:
                    return False
                string = f"{string[:i]}{self.functions[word][0] if type == 'function' else self.variables[word][0]}{string[j:]}"
                i += len(self.functions[word][0]) if type == 'function' else len(self.variables[word][0])
            else:
                i += 1
        return string

    def add_function(self, function_name, function_string, variable):
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
        # prompt for function name
        io.write("\nEnter the name of the function: -- 'exit' to cancel")
        while True:
            if len(io.inputs) == 0:  # pragma: no cover
                io.add_input("name: ")  # pragma: no cover
            function_name = io.read()
            if function_name == "exit":  # pragma: no cover
                return False  # pragma: no cover
            if not function_name.isidentifier():
                io.write("Invalid function name. Enter name like f_1\n")
                continue
            if function_name in self.functions or function_name in self.variables or function_name in ['af', 'av', 'variables', 'functions']:
                io.write("This name is already in use. Enter a new name\n")
                continue
            break

        variable = 'x'

        # prompt for function
        io.write("\nEnter the function. I.e. 'x**2'")
        while True:
            if len(io.inputs) == 0:  # pragma: no cover
                io.add_input("function: ")  # pragma: no cover
            function_string = io.read()
            if function_string == "exit":  # pragma: no cover
                return False  # pragma: no cover
            if self.check_and_replace(function_string, keep=variable) is False:
                io.write("Invalid function. Use expressions, functions, stored variables or 'x'\n")
                continue
            result = self.add_function(function_name, function_string, variable)
            if result is True:
                io.write(f"\nFunction '{function_name}' added successfully!\n")
                return
            io.write("Invalid expression\n")

    def add_variable_prompt(self, io):
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
            if variable_name in self.variables or variable_name in self.functions or variable_name in ['af', 'av', 'variables', 'functions']:
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
                return
            io.write("Invalid expression\n")

    def print_functions(self, io):
        io.write("\n")
        for name, value in self.functions.items():
            io.write(f"   {name}: {value[1]}")
        io.write("\n")
    
    def print_variables(self, io):
        io.write("\n")
        for name, value in self.variables.items():
            io.write(f"   {name}: {value[1]}")
        io.write("\n")