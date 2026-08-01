
def _attach_print_method(cls, sympy_name, func_name):
    meth_name = '_print_%s' % sympy_name
    if hasattr(cls, meth_name):
        raise ValueError("Edit method (or subclass) instead of overwriting.")
    def _print_method(self, expr):
        return '{}{}({})'.format(self._ns, func_name, ', '.join(map(self._print, expr.args)))
    _print_method.__doc__ = "Prints code for %s" % k
    setattr(cls, meth_name, _print_method)

