
def is_single_token(token_number, tokens):
    '''Is this a single token matching token_number followed by ENDMARKER, NL
    or NEWLINE tokens.
    '''
    return TOKEN_NUMBER(tokens[0]) == token_number and all(
        TOKEN_NUMBER(t) in (EM, NL, NEWLINE) for t in tokens[1:]
    )

