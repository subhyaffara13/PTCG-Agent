
def get_var(expr: Expression) -> Var:
    """
    Warning: this in only true for expressions captured by a match statement.
    Don't call it from anywhere else
    """
    assert isinstance(expr, NameExpr), expr
    node = expr.node
    assert isinstance(node, Var), node
    return node

