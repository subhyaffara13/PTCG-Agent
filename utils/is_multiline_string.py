
def is_multiline_string(token: tokenize.TokenInfo) -> bool:
    """Check if this is a multiline string."""
    return token.type in {FSTRING_END, TSTRING_END} or (
        token.type == tokenize.STRING and "\n" in token.string
    )

