class ServiceHandler:
    def __init__(self, io, translator):
        self.translator = translator
        self.io = io

    def run(self):
        self.info()
        while True:
            self.io.add_input("Command/expression: ", False)
            input = self.io.read()
            if input == "exit":
                break
            if input == "af":
                self.translator.add_function_prompt(self.io)
                continue
            result = self.translator.calculate(input)
            if result is False:
                self.io.write("\n!!!Invalid expression!!!\n")
            else:
                self.io.write(f"= {result}\n")

    def info(self):
        self.io.write("Enter an expression to calculate, i.e. '1 + (5-3)^2'\n\n")
        self.io.write("Available commands:\n")
        self.io.write("-    'exit' - quit the program\n")
        self.io.write("-    'af' - add a custom function\n")