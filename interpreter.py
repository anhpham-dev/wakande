from ast_nodes import Number, BinaryExpression, Variable, VariableDeclaration

def evaluate(node, environment):
    if isinstance(node, Number):
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