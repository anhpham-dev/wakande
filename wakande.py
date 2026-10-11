from lexer import Lexer
from parser import Parser
from interpreter import evaluate

source = "let 123 = 5"

lexer = Lexer(source)
tokens = lexer.tokenize()

parser = Parser(tokens)
ast = parser.parse()

environment = {}
result = evaluate(ast, environment)

print("Result:", result)
print("Variables:", environment)