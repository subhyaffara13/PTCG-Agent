
def code2ast(source):
    '''Convert a string object into an AST object.

    This function is retained for backwards compatibility, but it no longer
    attemps any conversions. It's equivalent to a call to ``ast.parse``.
    '''
    return ast.parse(source)

