# Wakande

## What is Wakande?
It's a small programming language built from scratch in Python.

Wakande is just a small experiment of mine to explore and understand how programming languages work :3. From reading the source code to evaluating expressions, I'm currently building the core components myself!

Wakande is still WIP btw.

## Example
```
let x = 10
let y = 20

x + y
```

Output:
```
20
```

## Current Features
Wakande currently supports:
- Variable declaration using let
- Integer and floating-point numbers
- Arithmetic operations: + - * /
- Parentheses for grouping expression
- Unary minus, including epxression like --5
- Variable references and evaluation
- Basic error reporting with line and column information in the lexer

## How it works?
1. Lexer (lexer.py)
- This would reads the source code and converts it into tokens, such as numbers, identifiers, operators and keywords
2. Parser (parser.py)
- Parser will take the tokens and build an abstract syntax tree (AST) that represents the structure of the program
3. AST nodes (ast_nodes.py)
- Defines the data structure that were used to represent numbers, binary expression, variables, declearation, and programs
4. Intepreter (interpreter.py)
- Evaluates the AST and then stores variable values in an environment

## Getting started
### Requirements: Python 3.10+
### Run the interpreter
Clone the repo:
```
git clone https://github.com/YOUR-USERNAME/wakande.git
cd wakande
```

Run the current entry point:
```
python wakande.py
```
The current wakande.py contains a sample program, so running it executes that program rather than opening any interactive prompts ;-;

## Current limitations
Wakande is still in its early stages. Some features that are not implemented yet include:
- Strings and string operations
- Conditional statements
- Loops
- Functions
- An interactive REPL
- A dedicated execution environment for source files
- More complete parser and runtime error handling
*I'm going to do this for Week 2 of Terra!*