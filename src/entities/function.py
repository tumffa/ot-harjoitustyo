class Function:
    """Class to store information about a function

    Attributes:
        name: the name of the function
        func: the global function name
        string: the function
        eval: the lambda function to evaluate
    """

    def __init__(self, name, global_function, string, evaluation):
        """Initializes the function with the given parameters"""

        self.name = name
        self.func = global_function
        self.string = string
        self.eval = evaluation

    def __str__(self):
        return f"{self.name}(x) = {self.string}"
