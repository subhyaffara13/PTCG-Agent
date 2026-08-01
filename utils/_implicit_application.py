
def _implicit_application(tokens: list[TOKEN | AppliedFunction], local_dict: DICT, global_dict: DICT):
    """Adds parentheses as needed after functions."""
    result: list[TOKEN | AppliedFunction] = []
    appendParen = 0  # number of closing parentheses to add
    skip = 0  # number of tokens to delay before adding a ')' (to
              # capture **, ^, etc.)
    exponentSkip = False  # skipping tokens before inserting parentheses to
                          # work with function exponentiation
    for tok, nextTok in zip(tokens, tokens[1:]):
        result.append(tok)
        if (tok[0] == NAME and nextTok[0] not in [OP, ENDMARKER, NEWLINE]):
            if _token_callable(tok, local_dict, global_dict, nextTok):  # type: ignore
                result.append((OP, '('))
                appendParen += 1
        # name followed by exponent - function exponentiation
        elif (tok[0] == NAME and nextTok[0] == OP and nextTok[1] == '**'):
            if _token_callable(tok, local_dict, global_dict):  # type: ignore
                exponentSkip = True
        elif exponentSkip:
            # if the last token added was an applied function (i.e. the
            # power of the function exponent) OR a multiplication (as
            # implicit multiplication would have added an extraneous
            # multiplication)
            if (isinstance(tok, AppliedFunction)
                or (tok[0] == OP and tok[1] == '*')):
                # don't add anything if the next token is a multiplication
                # or if there's already a parenthesis (if parenthesis, still
                # stop skipping tokens)
                if not (nextTok[0] == OP and nextTok[1] == '*'):
                    if not(nextTok[0] == OP and nextTok[1] == '('):
                        result.append((OP, '('))
                        appendParen += 1
                    exponentSkip = False
        elif appendParen:
            if nextTok[0] == OP and nextTok[1] in ('^', '**', '*'):
                skip = 1
                continue
            if skip:
                skip -= 1
                continue
            result.append((OP, ')'))
            appendParen -= 1

    if tokens:
        result.append(tokens[-1])

    if appendParen:
        result.extend([(OP, ')')] * appendParen)
    return result

