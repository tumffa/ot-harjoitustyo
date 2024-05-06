class Function:
    def __init__(self, name, global_function, string, evaluation):
        self.name = name
        self.func = global_function
        self.string = string
        self.eval = evaluation

    def __str__(self):
        return f"{self.name}(x) = {self.string}"
