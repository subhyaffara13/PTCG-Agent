
def _transform_equals_sign(tokens: list[TOKEN], local_dict: DICT, global_dict: DICT):
    """Transforms the equals sign ``=`` to instances of Eq.

    This is a helper function for ``convert_equals_signs``.
    Works with expressions containing one equals sign and no
    nesting. Expressions like ``(1=2)=False`` will not work with this
    and should be used with ``convert_equals_signs``.

    Examples: 1=2     to Eq(1,2)
              1*2=x   to Eq(1*2, x)

    This does not deal with function arguments yet.

    """
    result: list[TOKEN] = []
    if (OP, "=") in tokens:
        result.append((NAME, "Eq"))
        result.append((OP, "("))
        for token in tokens:
            if token == (OP, "="):
                result.append((OP, ","))
                continue
            result.append(token)
        result.append((OP, ")"))
    else:
        result = tokens
    return result

