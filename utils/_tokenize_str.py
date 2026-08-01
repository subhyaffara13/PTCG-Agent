
def _tokenize_str(code: str) -> list[TokenInfo]:
    return list(tokenize.generate_tokens(StringIO(code).readline))

