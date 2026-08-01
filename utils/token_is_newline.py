
def token_is_newline(token: tokenize.TokenInfo) -> bool:
    """Check if the token type is a newline token type."""
    return token[0] in NEWLINE

