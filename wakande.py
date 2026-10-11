from lexer import Lexer
from parser import Parser
from interpreter import evaluate

source = "let x = 10 + 5"
environment = {}

lexer = Lexer(source)
tokens = lexer.tokenize()

parser = Parser(tokens)
ast = parser.parse()

result = evaluate(ast, environment)
print(result, environment)

source = "let y = x * 2"

lexer = Lexer(source)
tokens = lexer.tokenize()

parser = Parser(tokens)
ast = parser.parse()

result = evaluate(ast, environment)
print(result, environment)

source = "y * 2 + 1"

lexer = Lexer(source)
tokens = lexer.tokenize()

parser = Parser(tokens)
ast = parser.parse()

result = evaluate(ast, environment)
print(result, environment)