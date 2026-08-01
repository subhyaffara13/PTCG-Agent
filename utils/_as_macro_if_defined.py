
def _as_macro_if_defined(meth):
    """ Decorator for printer methods

    When a Printer's method is decorated using this decorator the expressions printed
    will first be looked for in the attribute ``math_macros``, and if present it will
    print the macro name in ``math_macros`` followed by a type suffix for the type
    ``real``. e.g. printing ``sympy.pi`` would print ``M_PIl`` if real is mapped to float80.

    """
    @wraps(meth)
    def _meth_wrapper(self, expr, **kwargs):
        if expr in self.math_macros:
            return '%s%s' % (self.math_macros[expr], self._get_math_macro_suffix(real))
        else:
            return meth(self, expr, **kwargs)

    return _meth_wrapper

