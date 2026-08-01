
def evaluate_expression(expr: mypy.nodes.Expression) -> object:
    """Evaluate an expression at runtime.

    Return the result of the expression, or UNKNOWN if the expression cannot be
    evaluated.
    """
    return expr.accept(_evaluator)

