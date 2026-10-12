from ast_nodes import Number, BinaryExpression, Variable, VariableDeclaration, Program, UnaryExpression, Boolean, ComparisonExpression, IfStatement

def evaluate(node, environment):
    if isinstance(node, Program):
        result = None
        for statement in node.statements:
            result = evaluate(statement, environment)
        return result
    
    elif isinstance(node, IfStatement):
        condition = evaluate(node.condition, environment)
        if not isinstance(condition, bool):
            raise TypeError("An if condition must be a boolean")

        if condition:
            branch = node.then_branch
        else:
            branch = node.else_branch
        
        result = None

        if branch is not None:
            for statement in branch:
                result = evaluate(statement, environment)
        
        return result

    elif isinstance(node, Number):
        return node.value

    elif isinstance(node, BinaryExpression):
        left_val = evaluate(node.left, environment)

        if node.operator.kind == "AND":
            if not isinstance(left_val, bool):
                raise TypeError("'and' requires Boolean operands")
            if not left_val:
                return False
            
            right_val = evaluate(node.right, environment)
            if not isinstance(right_val, bool):
                raise TypeError("'and' requires a Boolean operands")
            
            return right_val
            
        elif node.operator.kind == "OR":
            if not isinstance(left_val, bool):
                raise TypeError("'or' requires Boolean operands")
            if left_val:
                return True
            
            right_val = evaluate(node.right, environment)
            if not isinstance(right_val, bool):
                raise TypeError("'or' requires a Boolean operands")

            return right_val
        
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
        if node.operator.kind == "NOT":
            if not isinstance(operand, bool):
                raise TypeError("'not' requires a Boolean operand")
            return not operand
    
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
            
    elif isinstance(node, Boolean):
        return node.value