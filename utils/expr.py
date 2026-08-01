
def expr(s: Scanner) -> ast.expr:
    ret = and_expr(s)
    while s.accept(TokenType.OR):
        rhs = and_expr(s)
        ret = ast.BoolOp(ast.Or(), [ret, rhs])
    return ret

