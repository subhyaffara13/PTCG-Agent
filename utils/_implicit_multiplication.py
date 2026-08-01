
def _implicit_multiplication(tokens: list[TOKEN | AppliedFunction], local_dict: DICT, global_dict: DICT):
    """Implicitly adds '*' tokens.

    Cases:

    - Two AppliedFunctions next to each other ("sin(x)cos(x)")

    - AppliedFunction next to an open parenthesis ("sin x (cos x + 1)")

    - A close parenthesis next to an AppliedFunction ("(x+2)sin x")\

    - A close parenthesis next to an open parenthesis ("(x+2)(x+3)")

    - AppliedFunction next to an implicitly applied function ("sin(x)cos x")

    """
    result: list[TOKEN | AppliedFunction] = []
    skip = False
    for tok, nextTok in zip(tokens, tokens[1:]):
        result.append(tok)
        if skip:
            skip = False
            continue
        if tok[0] == OP and tok[1] == '.' and nextTok[0] == NAME:
            # Dotted name. Do not do implicit multiplication
            skip = True
            continue
        if isinstance(tok, AppliedFunction):
            if isinstance(nextTok, AppliedFunction):
                result.append((OP, '*'))
            elif nextTok == (OP, '('):
                # Applied function followed by an open parenthesis
                if tok.function[1] == "Function":
                    tok.function = (tok.function[0], 'Symbol')
                result.append((OP, '*'))
            elif nextTok[0] == NAME:
                # Applied function followed by implicitly applied function
                result.append((OP, '*'))
        else:
            if tok == (OP, ')'):
                if isinstance(nextTok, AppliedFunction):
                    # Close parenthesis followed by an applied function
                    result.append((OP, '*'))
                elif nextTok[0] == NAME:
                    # Close parenthesis followed by an implicitly applied function
                    result.append((OP, '*'))
                elif nextTok == (OP, '('):
                    # Close parenthesis followed by an open parenthesis
                    result.append((OP, '*'))
            elif tok[0] == NAME and not _token_callable(tok, local_dict, global_dict):
                if isinstance(nextTok, AppliedFunction) or \
                    (nextTok[0] == NAME and _token_callable(nextTok, local_dict, global_dict)):
                    # Constant followed by (implicitly applied) function
                    result.append((OP, '*'))
                elif nextTok == (OP, '('):
                    # Constant followed by parenthesis
                    result.append((OP, '*'))
                elif nextTok[0] == NAME:
                    # Constant followed by constant
                    result.append((OP, '*'))
    if tokens:
        result.append(tokens[-1])
    return result

