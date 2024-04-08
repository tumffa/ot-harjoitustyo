class ServiceHandler:
    def __init__(self, io, translator):
        self.translator = translator
        self.io = io
    
    def run(self):
        while True:
            self.io.write("Enter expression, i.e. '1 + (5-3)^2' -- 'exit' to quit")
            self.io.add_input("", False)
            input = self.io.read()
            if input == "exit":
                break
            result = self.translator.calculate(input)
            if result is False:
                self.io.write("\n!!!Invalid expression!!!\n")
            else:
                self.io.write(f"= {result}\n")