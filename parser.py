from lexer import Lexer
from ast_nodes import Number, BinaryExpression, Variable, VariableDeclaration, Program

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
    
    def peek(self, offset=0):
        index = self.pos+offset
        return self.tokens[index]
    
    def advance(self):
        current_token = self.peek()
        self.pos += 1
        return current_token
    
    def parse_number(self):
        current_token = self.peek()
        if current_token.kind == "NUMBER":
            self.advance()
            return Number(value=current_token.value)
        else:
            raise ValueError("Token is not a number")

    def parse_expression(self):
        left = self.parse_term()
        while self.peek().kind in ("PLUS", "MINUS"):
            operation = self.advance()
            right = self.parse_term()
            left = BinaryExpression(left, operation, right)
        return left
        # return BinaryExpression(left, operation, right)

    def parse_factor(self):
        token = self.peek()
        if token.kind in ("EOF", "NEWLINE"):
            raise ValueError(f"Expected an expression at line {token.line}, column: {token.column}")

        if self.peek().kind == "NUMBER":
            return self.parse_number()
        elif self.peek().kind == "LPAREN":
            self.advance()
            expression = self.parse_expression()
            if self.peek().kind != "RPAREN":
                raise ValueError("Expected ')'")
            self.advance()
            return expression
        elif self.peek().kind == "IDENTIFIER":
            current_token = self.advance()
            return Variable(current_token.value)
        else:
            # token = self.peek()
            raise ValueError(f"Expected a number or '(', got {token.kind} at line {token.line}, column {token.column}")

    def parse_term(self):
        left = self.parse_factor()

        while self.peek().kind in ("STAR", "SLASH"):
            operation = self.advance()
            right = self.parse_factor()
            left = BinaryExpression(left, operation, right)

        return left
    
    def parse_variable_declaration(self):
        let = self.advance()
        token = self.peek()

        if self.peek().kind != "IDENTIFIER":
            raise ValueError(f"Expected a variable name, got {token.kind} at line {token.line}, column {token.column}")
        var_name = self.advance().value

        if self.peek().kind != "EQUALS":
            raise ValueError(f"Expected an equal sign, got {token.kind} at line {token.line}, column {token.column}")
        self.advance()

        initializer = self.parse_expression()
        return VariableDeclaration(var_name, initializer)

    def parse_statement(self):
        if self.peek().kind == "LET":
            return self.parse_variable_declaration()
        
        return self.parse_expression()

    def parse(self):
        return self.parse_program()
    
    def parse_program(self):
        statements = []
        while self.peek().kind != "EOF":
            if self.peek().kind == "NEWLINE":
                self.advance()
                continue    
            statements.append(self.parse_statement())
            if self.peek().kind == "NEWLINE":
                self.advance()
            elif self.peek().kind != "EOF":
                token = self.peek()
                raise ValueError(f"Expected newline or EOF, got {token.kind} at line {token.line}, column {token.column}")
            
        return Program(statements)
