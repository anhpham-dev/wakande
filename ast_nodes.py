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