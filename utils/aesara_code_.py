
def aesara_code_(expr, **kwargs):
    """ Wrapper for aesara_code that uses a new, empty cache by default. """
    kwargs.setdefault('cache', {})
    with warns_deprecated_sympy():
        return aesara_code(expr, **kwargs)

