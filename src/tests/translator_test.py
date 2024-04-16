import unittest
from services.translator import Translator


class TestTranslator(unittest.TestCase):
    def setUp(self):
        self.translator = Translator()

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
