
def _apply_functions(tokens: list[TOKEN | ParenthesisGroup], local_dict: DICT, global_dict: DICT):
    """Convert a NAME token + ParenthesisGroup into an AppliedFunction.

    Note that ParenthesisGroups, if not applied to any function, are
    converted back into lists of tokens.

    """
    result: list[TOKEN | AppliedFunction] = []
    symbol = None
    for tok in tokens:
        if isinstance(tok, ParenthesisGroup):
            if symbol and _token_callable(symbol, local_dict, global_dict):
                result[-1] = AppliedFunction(symbol, tok)
                symbol = None
            else:
                result.extend(tok)
        elif tok[0] == NAME:
            symbol = tok
            result.append(tok)
        else:
            symbol = None
            result.append(tok)
    return result

