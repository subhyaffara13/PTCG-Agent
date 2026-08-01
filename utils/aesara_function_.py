
def aesara_function_(inputs, outputs, **kwargs):
    """ Wrapper for aesara_function that uses a new, empty cache by default. """
    kwargs.setdefault('cache', {})
    with warns_deprecated_sympy():
        return aesara_function(inputs, outputs, **kwargs)

