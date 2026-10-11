from lexer import Lexer
from parser import Parser
from interpreter import evaluate

source = "let x = 10\nlet y = x * 2\nx * 3.1"

lexer = Lexer(source)
tokens = lexer.tokenize()

parser = Parser(tokens)
ast = parser.parse()

environment = {}
result = evaluate(ast, environment)

print("Result:", result)
print("Variables:", environment)