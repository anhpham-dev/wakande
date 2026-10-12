from ast_nodes import Number, BinaryExpression, Variable, VariableDeclaration, Program, UnaryExpression, ComparisonExpression

def evaluate(node, environment):
    if isinstance(node, Program):
        result = None
        for statement in node.statements:
            result = evaluate(statement, environment)
        return result
    
    elif isinstance(node, Number):
        return node.value

    elif isinstance(node, BinaryExpression):
        left_val = evaluate(node.left, environment)
        right_val = evaluate(node.right, environment)

        if node.operator.kind == "STAR":
            return left_val * right_val
        
        if node.operator.kind == "PLUS":
            return left_val + right_val

        if node.operator.kind == "MINUS":
            return left_val - right_val
        
        if node.operator.kind == "SLASH":
            return left_val / right_val
        
    elif isinstance(node, Variable):
        if node.name not in environment:
            raise ValueError(f"Undefined variable: {node.name}")
        return environment[node.name]
    
    elif isinstance(node, VariableDeclaration):
        value = evaluate(node.initializer, environment)
        environment[node.name] = value
        return value
    
    elif isinstance(node, UnaryExpression):
        operand = evaluate(node.operand, environment)

        if node.operator.kind == "MINUS":
            return -operand
    
    elif isinstance(node, ComparisonExpression):
        left_val = evaluate(node.left, environment)
        right_val = evaluate(node.right, environment)

        if node.operator.kind == "EQUAL_EQUAL":
            return left_val == right_val
        if node.operator.kind == "NOT_EQUAL":
            return left_val != right_val
        if node.operator.kind == "LESS":
            return left_val < right_val
        if node.operator.kind == "GREATER":
            return left_val > right_val
        if node.operator.kind == "LESS_EQUAL":
            return left_val <= right_val
        if node.operator.kind == "GREATER_EQUAL":
            return left_val >= right_val
            