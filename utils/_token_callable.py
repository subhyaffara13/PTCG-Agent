
def _token_callable(token: TOKEN, local_dict: DICT, global_dict: DICT, nextToken=None):
    """
    Predicate for whether a token name represents a callable function.

    Essentially wraps ``callable``, but looks up the token name in the
    locals and globals.
    """
    func = local_dict.get(token[1])
    if not func:
        func = global_dict.get(token[1])
    return callable(func) and not isinstance(func, Symbol)

