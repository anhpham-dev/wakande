from ast_nodes import ComparisonExpression
from lexer import Lexer
from ast_nodes import Number, BinaryExpression, Variable, VariableDeclaration, Program, UnaryExpression, Boolean, IfStatement

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

        if token.kind == "MINUS":
            operator = self.advance()
            operand = self.parse_factor()
            return UnaryExpression(operator, operand)
        elif token.kind == "NOT":
            operator = self.advance()
            operand = self.parse_factor()
            return UnaryExpression(operator, operand)
        elif token.kind == "TRUE":
            self.advance()
            return Boolean(True)
        elif token.kind == "FALSE":
            self.advance()
            return Boolean(False)
        elif self.peek().kind == "NUMBER":
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
            raise ValueError(f"Expected a number 1or '(', got {token.kind} at line {token.line}, column {token.column}")

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

        initializer = self.parse_or()
        return VariableDeclaration(var_name, initializer)

    def parse_statement(self):
        if self.peek().kind == "LET":
            return self.parse_variable_declaration()
        
        if self.peek().kind == "IF":
            return self.parse_if_statement()

        return self.parse_or()

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

    def parse_comparison(self):
        expression = self.parse_expression()
        comparison_operators = ["EQUAL_EQUAL", "NOT_EQUAL", "LESS", "GREATER", "LESS_EQUAL", "GREATER_EQUAL"]

        while self.peek().kind in comparison_operators:
            operator = self.advance()
            right = self.parse_expression()
            expression = ComparisonExpression(expression, operator, right)

        return expression
    
    def parse_and(self):
        expression = self.parse_comparison()

        while self.peek().kind == "AND":
            operator = self.advance()
            right = self.parse_comparison()
            expression = BinaryExpression(expression, operator, right)

        return expression
        
    def parse_or(self):
        expression = self.parse_and()
        while self.peek().kind == "OR":
            operator = self.advance()
            right = self.parse_and()
            expression = BinaryExpression(expression, operator, right)
        
        return expression
    
    def parse_block(self):
        if self.peek().kind != "LBRACE":
            token = self.peek()
            raise ValueError(f"Expected '{{', got {token.kind} at line {token.line}, column {token.column}")
        
        self.advance()
        statements = []
        while self.peek().kind not in ("RBRACE", "EOF"):
            if self.peek().kind == "NEWLINE":
                self.advance()
                continue

            statements.append(self.parse_statement())

            if self.peek().kind == "NEWLINE":
                self.advance()
            elif self.peek().kind not in ("RBRACE", "EOF"):
                token = self.peek()
                raise ValueError(f"Expected newline or '}}', got {token.kind} at line {token.line}, column {token.column}")
        
        if self.peek().kind == "EOF":
            token = self.peek()
            raise ValueError(f"Expected '}}' before end of input at line {token.line}, column: {token.column}")

        self.advance()
        return statements
    

    def parse_if_statement(self):
        self.advance()
        condition = self.parse_or()
        then_branch = self.parse_block()
        else_branch = None

        if self.peek().kind == "ELSE":
            self.advance()
            else_branch = self.parse_block()
        
        return IfStatement(condition=condition, then_branch=then_branch, else_branch=else_branch)
