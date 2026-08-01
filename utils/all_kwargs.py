
def all_kwargs(s: Scanner) -> list[ast.keyword]:
    ret = [single_kwarg(s)]
    while s.accept(TokenType.COMMA):
        ret.append(single_kwarg(s))
    return ret

