from dataclasses import dataclass

@dataclass
class Number:
    value: int | float

@dataclass
class BinaryExpression:
    left: object
    operator: str
    right: object

@dataclass
class Variable:
    name: str

@dataclass
class VariableDeclaration:
    name: str
    initializer: object

@dataclass
class Program:
    statements: list

@dataclass
class UnaryExpression:
    operator: object
    operand: object

@dataclass
class ComparisonExpression:
    left: object
    operator: object
    right: object

@dataclass
class Boolean:
    value: bool