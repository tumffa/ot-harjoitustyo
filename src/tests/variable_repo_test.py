import unittest
from repositories.variable_repository import VariableRepository


class TestVariableRepository(unittest.TestCase):
    def setUp(self):
        commands = ['exit', 'af', 'av', 'variables', 'functions', 'solve']
        self.v_repo = VariableRepository(commands)

    def test_add_variable(self):
        self.v_repo.add_variable('x', '2', '2')
        self.assertEqual(self.v_repo.get_variables()['x'], '2')

    def test_check_identifier_existing_name(self):
        self.assertEqual(self.v_repo.check_identifier('e')[0], False)

    def test_check_identifier_invalid_name(self):
        self.assertEqual(self.v_repo.check_identifier('f-1')[0], False)

    def test_check_identifier_valid_name(self):
        self.assertEqual(self.v_repo.check_identifier('f_1')[0], True)

    def test_get_variables(self):
        self.assertEqual(self.v_repo.get_variables(),
                         {'e': 'math.e', 'pi': 'math.pi'})