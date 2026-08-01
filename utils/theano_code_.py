
def theano_code_(expr, **kwargs):
    """ Wrapper for theano_code that uses a new, empty cache by default. """
    kwargs.setdefault('cache', {})
    with warns_deprecated_sympy():
        return theano_code(expr, **kwargs)

