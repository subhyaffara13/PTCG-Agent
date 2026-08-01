
def _is_empty_generator_function(func: FuncItem) -> bool:
    """
    Checks whether a function's body is 'return; yield' (the yield being added only
    to promote the function into a generator function).
    """
    body = func.body.body
    return (
        len(body) == 2
        and isinstance(ret_stmt := body[0], ReturnStmt)
        and (ret_stmt.expr is None or is_literal_none(ret_stmt.expr))
        and isinstance(expr_stmt := body[1], ExpressionStmt)
        and isinstance(yield_expr := expr_stmt.expr, YieldExpr)
        and (yield_expr.expr is None or is_literal_none(yield_expr.expr))
    )

