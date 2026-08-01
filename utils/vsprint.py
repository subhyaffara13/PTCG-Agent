
def vsprint(expr, **settings):
    r"""Function for displaying expressions generated in the
    sympy.physics vector package.

    Returns the output of vprint() as a string.

    Parameters
    ==========

    expr : valid SymPy object
        SymPy expression to print
    settings : args
        Same as the settings accepted by SymPy's sstr().

    Examples
    ========

    >>> from sympy.physics.vector import vsprint, dynamicsymbols
    >>> u1, u2 = dynamicsymbols('u1 u2')
    >>> u2d = dynamicsymbols('u2', level=1)
    >>> print("%s = %s" % (u1, u2 + u2d))
    u1(t) = u2(t) + Derivative(u2(t), t)
    >>> print("%s = %s" % (vsprint(u1), vsprint(u2 + u2d)))
    u1 = u2 + u2'

    """

    string_printer = VectorStrPrinter(settings)
    return string_printer.doprint(expr)

