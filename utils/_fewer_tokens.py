
def _fewer_tokens(tokens, remove):
    '''Process the output of `tokenize.generate_tokens` removing
    the tokens specified in `remove`.
    '''
    for values in tokens:
        if values[0] in remove:
            continue
        yield values

