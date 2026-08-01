
def and_expr(s: Scanner) -> ast.expr:
    ret = not_expr(s)
    while s.accept(TokenType.AND):
        rhs = not_expr(s)
        ret = ast.BoolOp(ast.And(), [ret, rhs])
    return ret

