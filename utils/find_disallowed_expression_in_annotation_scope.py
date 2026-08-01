
def find_disallowed_expression_in_annotation_scope(expr: ast3.expr | None) -> ast3.expr | None:
    if expr is None:
        return None
    for node in ast3.walk(expr):
        if isinstance(node, (ast3.Yield, ast3.YieldFrom, ast3.NamedExpr, ast3.Await)):
            return node
    return None

