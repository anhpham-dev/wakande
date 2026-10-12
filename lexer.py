from dataclasses import dataclass
from typing import Any

@dataclass
class Token:
    kind: str
    value: Any
    line: int
    column: int

class Lexer:
    def __init__(self, source: str):
        self.SINGLE_CHAR_TOKEN = {
            "+": "PLUS",
            "-": "MINUS",
            "*": "STAR",
            "/": "SLASH",
            "(": "LPAREN",
            ")": "RPAREN",
            "=": "EQUALS",
            "<": "LESS",
            ">": "GREATER",
            "{": "LBRACE",
            "}": "RBRACE",
        }
        self.DOUBLE_CHAR_TOKEN = {
            "==": "EQUAL_EQUAL",
            "!=": "NOT_EQUAL",
            "<=": "LESS_EQUAL",
            ">=": "GREATER_EQUAL",
        }
        self.KEYWORDS = {
            "let": "LET",
            "true": "TRUE",
            "false": "FALSE",
            "and": "AND",
            "or": "OR",
            "not": "NOT",
            "if": "IF",
            "else": "ELSE",
        }
        self.source = source
        self.line = 1
        self.column = 1
        self.pos = 0

    def peek(self, offset=0):
        index = self.pos + offset
        return self.source[index] if index < len(self.source) else "\0"

    def advance(self):
        current_char = self.peek()
        if current_char == "\n":
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        self.pos += 1
        return current_char

    def read_numbers(self):
        start_line = self.line
        start_column = self.column
        is_float = False
        digits = []
        
        while self.peek().isdigit():
            digits.append(self.advance())
        
        if self.peek() == "." and self.peek(1).isdigit():
            is_float = True
            digits.append(self.advance())

            while self.peek().isdigit():
                digits.append(self.advance())
            
        if self.peek().isalpha() or self.peek() == "_":
            raise ValueError(f"Invalid Number Identifier at line: {start_line}, column: {start_column}")

        text = "".join(digits)
        value = float(text) if is_float else int(text)

        return Token("NUMBER", value, start_line, start_column)
    
    def next_token(self):
        while self.peek() in [" ", "\t", "\r"]:
            self.advance()
        
        if self.peek() == "\n":
            line = self.line
            col = self.column
            self.advance()
            return Token("NEWLINE", "\n", line, col)

        line = self.line
        col = self.column
        current_char = self.peek()

        if current_char == "\0":
            return Token("EOF", None, line, col)
        elif current_char.isdigit():
            return self.read_numbers()
        elif current_char + self.peek(1) in self.DOUBLE_CHAR_TOKEN:
            operator = self.advance() + self.advance()
            return Token(self.DOUBLE_CHAR_TOKEN[operator], operator, line, col)
        elif current_char in self.SINGLE_CHAR_TOKEN:
            char = self.advance()
            return Token(self.SINGLE_CHAR_TOKEN[char], char, line, col)
        elif current_char.isalpha() or current_char == "_":
            return self.read_identifier()
        else:
            raise ValueError(f"Invalid Character '{current_char!r}' at line: {line}, column: {col}")

    def tokenize(self):
        tokens = []

        while True:
            token = self.next_token()
            tokens.append(token)
            if token.kind == "EOF":
                break
        
        return tokens

    def read_identifier(self):
        start_line = self.line
        start_column = self.column
        chars = []

        if not self.peek().isalpha() and self.peek() != "_":
            raise ValueError(f"Invalid Variables Define")

        while self.peek().isalnum() or self.peek() == "_":
            chars.append(self.advance())
        
        word = "".join(chars)
        kind = self.KEYWORDS.get(word, "IDENTIFIER")

        return Token(kind, word, start_line, start_column)



# if __name__ == "__main__":
    # token = []
    # token.append(Token(kind="NUMBER", value=25, line=1, column=1))
    # token.append(Token(kind="IDENTIFIER", value="total", line=1, column=5))
    # token.append(Token(kind="PLUS", value=None, line=1, column=14))
    # token.append(Token(kind="STRING", value="Hello, World!", line=2, column=7))

    # print(token)


    # lexer = Lexer("12 + 5")
    
    # print(lexer.peek())
    # print(lexer.pos)
    # print()
    # print(lexer.advance())
    # print(lexer.pos)
    # print()
    # print(lexer.peek())
    # print()
    
    # lexer = Lexer("A")
    # lexer.advance()
    # print(repr(lexer.peek()))


    # lexer = Lexer("a\nbc")
    # print(lexer.advance())
    # print(lexer.line, lexer.column)
    # print(repr(lexer.advance()))
    # print(lexer.line, lexer.column)
    # print(lexer.advance())
    # print(lexer.line, lexer.column)


    # lexer = Lexer("123 + 4.56")

    # print(lexer.read_numbers())

    # lexer.advance()
    # lexer.advance()
    # lexer.advance()
    
    # print(lexer.read_numbers())


    # source = "123 + 4.5 * (2 - 1)"
    # lexer = Lexer(source)

    # for token in lexer.tokenize():
    #     print(token)

    # source = "let money = 1029173"
    # lexer = Lexer(source)

    # for token in lexer.tokenize():
    #     print(token)