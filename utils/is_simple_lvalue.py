
def is_simple_lvalue(expr: Expression) -> bool:
    return not isinstance(expr, (StarExpr, ListExpr, TupleExpr))

