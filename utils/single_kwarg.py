
def single_kwarg(s: Scanner) -> ast.keyword:
    keyword_name = s.accept(TokenType.IDENT, reject=True)
    if not keyword_name.value.isidentifier():
        raise SyntaxError(
            f"not a valid python identifier {keyword_name.value}",
            (FILE_NAME, 1, keyword_name.pos + 1, s.input),
        )
    if keyword.iskeyword(keyword_name.value):
        raise SyntaxError(
            f"unexpected reserved python keyword `{keyword_name.value}`",
            (FILE_NAME, 1, keyword_name.pos + 1, s.input),
        )
    s.accept(TokenType.EQUAL, reject=True)

    if value_token := s.accept(TokenType.STRING):
        value: str | int | bool | None = value_token.value[1:-1]  # strip quotes
    else:
        value_token = s.accept(TokenType.IDENT, reject=True)
        if (number := value_token.value).isdigit() or (
            number.startswith("-") and number[1:].isdigit()
        ):
            value = int(number)
        elif value_token.value in BUILTIN_MATCHERS:
            value = BUILTIN_MATCHERS[value_token.value]
        else:
            raise SyntaxError(
                f'unexpected character/s "{value_token.value}"',
                (FILE_NAME, 1, value_token.pos + 1, s.input),
            )

    ret = ast.keyword(keyword_name.value, ast.Constant(value))
    return ret

