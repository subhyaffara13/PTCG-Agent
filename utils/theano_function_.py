
def theano_function_(inputs, outputs, **kwargs):
    """ Wrapper for theano_function that uses a new, empty cache by default. """
    kwargs.setdefault('cache', {})
    with warns_deprecated_sympy():
        return theano_function(inputs, outputs, **kwargs)

