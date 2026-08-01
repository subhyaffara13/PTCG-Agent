
def expression(s: Scanner) -> ast.Expression:
    if s.accept(TokenType.EOF):
        ret: ast.expr = ast.Constant(False)
    else:
        ret = expr(s)
        s.accept(TokenType.EOF, reject=True)
    return ast.fix_missing_locations(ast.Expression(ret))

