import math
import random
import string as s

class Translator:
    def __init__(self):
        self.functions = {
            'abs': 'abs',
            'sqrt': 'math.sqrt',
            'exp': 'math.exp'
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
            if string[i].isalpha():
                j = i
                while j < len(string) and string[j].isalpha():
                    j += 1
                word = string[i:j]
                if word == keep:
                    i = j
                    continue
                if word not in self.functions:
                    return False
                string = string[:i] + self.functions[word] + string[j:]
                i += len(self.functions[word])
            else:
                i += 1
        return string

    def add_function(self, function_name, function_string, variable):
        function_string = function_string.replace("^", "**")
        # check for injection
        function_string = self.check_and_replace(function_string, keep=variable)
        # generate a random string to use as the function name
        random_string = ''.join(random.choices(s.ascii_letters, k=10))
        try:
            # check if the function is valid
            result = eval(f'lambda {variable}: {function_string}') # pylint: disable=eval-used
        except:
            return False
        # save the actual function with random identifier
        globals()[random_string] = result
        self.functions[function_name] = random_string
        return True

    def add_function_prompt(self, io):
        # prompt for function name
        io.write("Enter the name of the function: -- 'exit' to cancel\n")
        while True:
            if len(io.inputs) == 0:  # pragma: no cover
                io.add_input("name: ")  # pragma: no cover
            function_name = io.read()
            if function_name == "exit":  # pragma: no cover
                return False  # pragma: no cover
            if not function_name.isidentifier():
                io.write("Invalid function name. Enter name like f_1\n")
                continue
            if function_name in self.functions:
                io.write("Function name already exists. Enter a new name\n")
                continue
            break

        variable = 'x'

        # prompt for function
        io.write("Enter the function. I.e. 'x**2'\n")
        while True:
            if len(io.inputs) == 0:  # pragma: no cover
                io.add_input("function: ")  # pragma: no cover
            function_string = io.read()
            if function_string == "exit":  # pragma: no cover
                return False  # pragma: no cover
            if self.check_and_replace(function_string, keep=variable) is False:
                io.write("Invalid function. Use expressions, functions or x\n")
                continue
            result = self.add_function(function_name, function_string, variable)
            if result is True:
                io.write(f"Function '{function_name}' added successfully!\n")
                return
            io.write("Invalid expression\n")
