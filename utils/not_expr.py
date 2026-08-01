
def not_expr(s: Scanner) -> ast.expr:
    if s.accept(TokenType.NOT):
        return ast.UnaryOp(ast.Not(), not_expr(s))
    if s.accept(TokenType.LPAREN):
        ret = expr(s)
        s.accept(TokenType.RPAREN, reject=True)
        return ret
    ident = s.accept(TokenType.IDENT)
    if ident:
        name = ast.Name(IDENT_PREFIX + ident.value, ast.Load())
        if s.accept(TokenType.LPAREN):
            ret = ast.Call(func=name, args=[], keywords=all_kwargs(s))
            s.accept(TokenType.RPAREN, reject=True)
        else:
            ret = name
        return ret

    s.reject((TokenType.NOT, TokenType.LPAREN, TokenType.IDENT))

