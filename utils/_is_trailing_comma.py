import itertools

def _is_trailing_comma(tokens: list[tokenize.TokenInfo], index: int) -> bool:
    """Check if the given token is a trailing comma.

    :param tokens: Sequence of modules tokens
    :type tokens: list[tokenize.TokenInfo]
    :param int index: Index of token under check in tokens
    :returns: True if the token is a comma which trails an expression
    :rtype: bool
    """
    token = tokens[index]
    if token.exact_type != tokenize.COMMA:
        return False
    # Must have remaining tokens on the same line such as NEWLINE
    left_tokens = itertools.islice(tokens, index + 1, None)

    more_tokens_on_line = False
    for remaining_token in left_tokens:
        if remaining_token.start[0] == token.start[0]:
            more_tokens_on_line = True
            # If one of the remaining same line tokens is not NEWLINE or COMMENT
            # the comma is not trailing.
            if remaining_token.type not in (tokenize.NEWLINE, tokenize.COMMENT):
                return False

    if not more_tokens_on_line:
        return False

    def get_curline_index_start() -> int:
        """Get the index denoting the start of the current line."""
        for subindex, token in enumerate(reversed(tokens[:index])):
            # See Lib/tokenize.py and Lib/token.py in cpython for more info
            if token.type == tokenize.NEWLINE:
                return index - subindex
        return 0

    curline_start = get_curline_index_start()
    expected_tokens = {"return", "yield"}
    return any(
        "=" in prevtoken.string or prevtoken.string in expected_tokens
        for prevtoken in tokens[curline_start:index]
    )

