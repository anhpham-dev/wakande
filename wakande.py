from lexer import Lexer
from parser import Parser
from interpreter import evaluate

source = """
let x = 15
let y = 10
let z = 3 * x

z + x / y > 14

"""

lexer = Lexer(source)
tokens = lexer.tokenize()

parser = Parser(tokens)
ast = parser.parse()

environment = {}
result = evaluate(ast, environment)

print("Result:", result)
print("Variables:", environment)    