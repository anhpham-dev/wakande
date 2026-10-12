import unittest

from lexer import Lexer
from parser import Parser
from interpreter import evaluate
from ast_nodes import ComparisonExpression

def run_source(source):
    tokens = Lexer(source).tokenize()
    ast = Parser(tokens).parse()

    environment = {}
    result = evaluate(ast, environment)

    return result, environment

class TestInterpreter(unittest.TestCase):
    def test_add(self):
        result, _ = run_source("2 + 3")
        self.assertEqual(result, 5)
    
    def test_operator_precedence(self):
        result, _ = run_source("2 + 3 * 4")
        self.assertEqual(result, 14)
    
    def test_parentheses(self):
        result, _ = run_source("(2 + 3) * 4")
        self.assertEqual(result, 20)
    
    def test_unary_minus(self):
        result, _ = run_source("-5")
        self.assertEqual(result, -5)

    def test_double_negative(self):
        result, _ = run_source("10 - -3")
        self.assertEqual(result, 13)

    def test_division(self):
        result, _ = run_source("10 / 4")
        self.assertEqual(result, 2.5)
    
    def variable(self):
        result, variables = run_source("let x = 10\nlet y = x + 2\ny")
        self.assertEqual(result, 12)
        self.assertEqual(variables, {"x": 10, "y": 12})
    
    def test_undefined_variable(self):
        with self.assertRaisesRegex(ValueError, "Undefined variable"):
            run_source("sigma + 5")
    
    def test_comparison_tokens(self):
        tokens = Lexer("== != < > <= >=").tokenize()
        kinds = [token.kind for token in tokens]

        self.assertEqual(kinds, ["EQUAL_EQUAL", "NOT_EQUAL", "LESS", "GREATER", "LESS_EQUAL", "GREATER_EQUAL", "EOF"])
    
    def test_assignment_equals_is_still_distinct(self):
        tokens = Lexer("let x = 5").tokenize()
        kinds = [token.kind for token in tokens]

        self.assertEqual(kinds, ["LET", "IDENTIFIER", "EQUALS", "NUMBER", "EOF"])

    def test_comparison_parsing(self):
        tokens = Lexer("5 < 10").tokenize()
        ast = Parser(tokens).parse()

        self.assertIsInstance(ast.statements[0], ComparisonExpression)
        self.assertEqual(ast.statements[0].operator.kind, "LESS")

    def test_equal(self):
        result, _ = run_source("5 == 5")
        self.assertIs(result, True)

    def test_not_equal(self):
        result, _ = run_source("5 != 3")
        self.assertIs(result, True)

    def test_less_than(self):
        result, _ = run_source("3 < 5")
        self.assertIs(result, True)

    def test_greater_than(self):
        result, _ = run_source("8 > 10")
        self.assertIs(result, False)

    def test_less_equal(self):
        result, _ = run_source("5 <= 5")
        self.assertIs(result, True)

    def test_greater_equal(self):
        result, _ = run_source("5 >= 8")
        self.assertIs(result, False)

    def test_comparison_with_arithmetic(self):
        result, _ = run_source("2 + 3 < 10")
        self.assertIs(result, True)

    def test_comparison_with_variables(self):
        result, _ = run_source("let x = 10\n x >= 10")
        self.assertIs(result, True)

if __name__ == "__main__":
    unittest.main()