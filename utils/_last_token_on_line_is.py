
def _last_token_on_line_is(tokens: TokenWrapper, line_end: int, token: str) -> bool:
    return (line_end > 0 and tokens.token(line_end - 1) == token) or (
        line_end > 1
        and tokens.token(line_end - 2) == token
        and tokens.type(line_end - 1) == tokenize.COMMENT
    )

