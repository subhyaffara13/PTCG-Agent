
def is_eol_token(token: tokenize.TokenInfo) -> bool:
    """Check if the token is an end-of-line token."""
    return token[0] in NEWLINE or token[4][token[3][1] :].lstrip() == "\\\n"

