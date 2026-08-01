
def factorial_notation(tokens: list[TOKEN], local_dict: DICT, global_dict: DICT):
    """Allows standard notation for factorial."""
    result: list[TOKEN] = []
    nfactorial = 0
    for toknum, tokval in tokens:
        if toknum == OP and tokval == "!":
            # In Python 3.12 "!" are OP instead of ERRORTOKEN
            nfactorial += 1
        elif toknum == ERRORTOKEN:
            op = tokval
            if op == '!':
                nfactorial += 1
            else:
                nfactorial = 0
                result.append((OP, op))
        else:
            if nfactorial == 1:
                result = _add_factorial_tokens('factorial', result)
            elif nfactorial == 2:
                result = _add_factorial_tokens('factorial2', result)
            elif nfactorial > 2:
                raise TokenError
            nfactorial = 0
            result.append((toknum, tokval))
    return result

