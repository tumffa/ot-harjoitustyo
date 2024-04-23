class ServiceHandler:
    def __init__(self, io, translator):
        self.translator = translator
        self.io = io

    def run(self):
        self.info()
        while True:
            self.io.add_input("Command/expression: ", False)
            input = self.io.read() # pylint: disable=redefined-builtin
            # built-in input is redefined to allow for easier testing
            if input == "exit":
                break
            if input == "af":
                self.translator.add_function_prompt(self.io)
                continue
            if input == "av":
                self.translator.add_variable_prompt(self.io)
                continue
            if input == "variables":
                self.translator.print_variables(self.io)
                continue
            if input == "functions":
                self.translator.print_functions(self.io)
                continue
            result = self.translator.calculate(input)
            if result is False:
                self.io.write("\n!!!Invalid expression!!!\n")
            else:
                self.io.write(f"= {result}\n")
            

    def info(self):
        self.io.write("Enter an expression to calculate, i.e. '1 + (5-3)^2'\n\n")
        self.io.write("Available commands:\n")
        self.io.write("    'exit' - quit the program\n")
        self.io.write("\n")
        self.io.write("    'af' - add a custom function\n")
        self.io.write("    'av' - store a value into a variable\n")
        self.io.write("\n")
        self.io.write("    'variables' - print stored variables\n")
        self.io.write("    'functions' - print stored functions\n")
