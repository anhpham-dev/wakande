from lexer import Lexer

source = "5 == 5\n3 != 4\n2 < 3\n4 > 2\n5 <= 5\n6 >= 7"

for token in Lexer(source).tokenize():
    print(token.kind)