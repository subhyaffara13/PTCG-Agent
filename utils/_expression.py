
def _expression(initial, tokens, data):
    """
    Consume some number of tokens and return a balanced PostScript expression.

    Parameters
    ----------
    initial : _Token
        The token that triggered parsing a balanced expression.
    tokens : iterator of _Token
        Following tokens.
    data : bytes
        Underlying data that the token positions point to.

    Returns
    -------
    _BalancedExpression
    """
    delim_stack = []
    token = initial
    while True:
        if token.is_delim():
            if token.raw in ('[', '{'):
                delim_stack.append(token)
            elif token.raw in (']', '}'):
                if not delim_stack:
                    raise RuntimeError(f"unmatched closing token {token}")
                match = delim_stack.pop()
                if match.raw != token.opposite():
                    raise RuntimeError(
                        f"opening token {match} closed by {token}"
                    )
                if not delim_stack:
                    break
            else:
                raise RuntimeError(f'unknown delimiter {token}')
        elif not delim_stack:
            break
        token = next(tokens)
    return _BalancedExpression(
        initial.pos,
        data[initial.pos:token.endpos()].decode('ascii', 'replace')
    )

