
def _tokenize_files_to_codes_mapping(value: str) -> list[_Token]:
    tokens = []
    i = 0
    while i < len(value):
        for token_re, token_name in _FILE_LIST_TOKEN_TYPES:
            match = token_re.match(value, i)
            if match:
                tokens.append(_Token(token_name, match.group().strip()))
                i = match.end()
                break
        else:
            raise AssertionError("unreachable", value, i)
    tokens.append(_Token(_EOF, ""))

    return tokens

