
def describe_token(token: "Token") -> str:
    """Returns a description of the token."""
    if token.type == TOKEN_NAME:
        return token.value

    return _describe_token_type(token.type)

