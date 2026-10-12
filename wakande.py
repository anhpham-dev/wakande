from lexer import Lexer
from parser import Parser
from interpreter import evaluate

source = """
let age = 16
let has_permission = true

age >= 18 or has_permission
"""

lexer = Lexer(source)
tokens = lexer.tokenize()

parser = Parser(tokens)
ast = parser.parse()

environment = {}
result = evaluate(ast, environment)

print("Result:", result)
print("Variables:", environment)    