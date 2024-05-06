import unittest
from services.translator import Translator
from services.consoleio import ConsoleIO
from repositories.function_repository import FunctionRepository
from repositories.variable_repository import VariableRepository

class TestTranslator(unittest.TestCase):
    def setUp(self):
        commands = ['exit', 'af', 'av', 'variables', 'functions', 'solve']
        f_repo = FunctionRepository(commands)
        v_repo = VariableRepository(commands)
        self.translator = Translator(f_repo, v_repo)
        io = ConsoleIO(['f', 'x + 2', 'exit'])
        self.translator.add_function_prompt(io)
        io = ConsoleIO(['g', 'x**2', 'exit'])
        self.translator.add_function_prompt(io)
        io = ConsoleIO(['var', '5', 'exit'])
        self.translator.add_variable_prompt(io)
        
    def test_calculate_with_correct_operators(self):
        expression = "(((2 + 2 + 6) * (1/5))^2)^2"
        result = 16
        self.assertEqual(self.translator.calculate(expression), result)

    def test_calculate_with_invalid_expression(self):
        expression = "2 + 5)"
        result = False
        self.assertEqual(self.translator.calculate(expression), result)

    def test_calculate_with_letters(self):
        expression = "twoplustwoisfour"
        result = False
        self.assertEqual(self.translator.calculate(expression), result)

    def test_check_and_replace_allows_functions(self):
        expression = "f(2) + g(2) + abs(-2) + exp(0) + sqrt(4)"
        result = 13
        self.assertEqual(self.translator.calculate(expression), result)

    def test_add_function_prompt_with_valid_input(self):
        io = ConsoleIO(["j", "x*2"])
        self.translator.add_function_prompt(io)
        self.assertEqual(self.translator.calculate("j(2)"), 4)

    def test_add_function_prompt_with_bad_identifier(self):
        io = ConsoleIO(["f-1", "exit"])
        self.translator.add_function_prompt(io)
        self.assertIn(
            "Invalid function name. Enter name like f_1\n",
            io.outputs)
        
    def test_add_function_prompt_with_existing_name(self):
        io = ConsoleIO(["f", "exit"])
        self.translator.add_function_prompt(io)
        self.assertIn(
            "This name is already in use. Enter a new name\n",
            io.outputs)
        
    def test_add_function_prompt_with_invalid_function(self):
        io = ConsoleIO(["j", "2x", "exit"])
        self.translator.add_function_prompt(io)
        self.assertIn("Invalid expression!\n", io.outputs)
        
    def test_add_variable_prompt_with_bad_identifier(self):
        io = ConsoleIO(["f-1", "exit"])
        self.translator.add_variable_prompt(io)
        self.assertIn(
            "Invalid variable name. Enter name like 'var'\n",
            io.outputs)
        
    def test_add_variable_prompt_with_existing_name(self):
        io = ConsoleIO(["var", "exit"])
        self.translator.add_variable_prompt(io)
        self.assertIn(
            "This name is already in use. Enter a new name\n",
            io.outputs)
        
    def test_add_variable_prompt_with_valid_input(self):
        io = ConsoleIO(["var2", "3*g(2)-e^0", "exit"])
        self.translator.add_variable_prompt(io)
        self.assertEqual(self.translator.calculate("var2"), 11)

    def test_print_variables(self):
        io = ConsoleIO()
        self.translator.print_variables(io)
        self.assertIn(f"   var = 5", io.outputs)

    def test_print_functions(self):
        io = ConsoleIO()
        self.translator.print_functions(io)
        self.assertIn(f"   f(x) = x + 2", io.outputs)

    def test_solve_equation_prompt_valid_input(self):
        io = ConsoleIO(["x^2 = 9", "exit"])
        self.translator.solve_equation_prompt(io)
        self.assertIn("\nSolution: [-3, 3]\n", io.outputs)

    def test_solve_equation_prompt_no_solution(self):
        io = ConsoleIO(["2*2**x = 2**x", "exit"])
        self.translator.solve_equation_prompt(io)
        self.assertIn("No solution\n", io.outputs)

    def test_solve_equation_prompt_with_function(self):
        io = ConsoleIO(["2*f(x) = 2", "exit"])
        result = self.translator.solve_equation_prompt(io)
        self.assertEqual(result, False)

    def test_solve_equation_prompt_with_invalid_expression(self):
        io = ConsoleIO(["2x = 2", "exit"])
        result = self.translator.solve_equation_prompt(io)
        self.assertEqual(result, False)

    def test_solve_equation_prompt_with_injection(self):
        io = ConsoleIO(["db = 0", "exit"])
        result = self.translator.solve_equation_prompt(io)
        self.assertEqual(result, False)

    def test_solve_equation_without_equalsign(self):
        io = ConsoleIO(["2x + 2", "exit"])
        self.translator.solve_equation_prompt(io)
        self.assertIn("Invalid equation. Use ' = ' to separate the left and right sides\n", io.outputs)