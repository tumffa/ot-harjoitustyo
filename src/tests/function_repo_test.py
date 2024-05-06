import unittest
from repositories.function_repository import FunctionRepository

class TestFunctionRepository(unittest.TestCase):
    def setUp(self):
        commands = ['exit', 'af', 'av', 'variables', 'functions', 'solve']
        self.f_repo = FunctionRepository(commands)

    def test_add_function(self):
        self.f_repo.add_function("f", "x + 2", 'aabbcc', '')
        self.assertEqual(self.f_repo.get_functions()['f'],
                          ('aabbcc', 'x + 2'))
        
    def test_check_identifier_existing_name(self):
        self.assertEqual(self.f_repo.check_identifier('abs')[0], False)

    def test_check_identifier_invalid_name(self):
        self.assertEqual(self.f_repo.check_identifier('f-1')[0], False)

    def test_check_identifier_valid_name(self):
        self.assertEqual(self.f_repo.check_identifier('f_1')[0], True)

    def test_get_functions(self):
        self.assertEqual(self.f_repo.get_functions(),
                            {'abs': ('abs', 'abs(x)'),
                             'sqrt': ('math.sqrt', 'math.sqrt(x)'),
                             'exp': ('math.exp', 'math.exp(x)'),
                             'sin': ('math.sin', 'math.sin(x)'),
                             'cos': ('math.cos', 'math.cos(x)')})