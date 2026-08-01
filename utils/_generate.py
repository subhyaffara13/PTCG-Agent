
def _generate(code):
    '''Pass the code into `tokenize.generate_tokens` and convert the result
    into a list.
    '''
    # tokenize.generate_tokens is an undocumented function accepting text
    return list(tokenize.generate_tokens(io.StringIO(code).readline))

