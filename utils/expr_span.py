
def expr_span(expr: Expression) -> str:
    """Format expression span as in mypy error messages."""
    return f"{expr.line}:{expr.column + 1}:{expr.end_line}:{expr.end_column}"

