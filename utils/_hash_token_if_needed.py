
def _hash_token_if_needed(token: str) -> str:
    """
    Hash the token if it's a string and starts with "sk-"

    Else return the token as is
    """
    if token.startswith("sk-"):
        return hash_token(token=token)
    else:
        return token

