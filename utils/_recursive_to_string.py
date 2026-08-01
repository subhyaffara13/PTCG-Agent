
def _recursive_to_string(doprint, arg):
    """Functions in lambdify accept both SymPy types and non-SymPy types such as python
    lists and tuples. This method ensures that we only call the doprint method of the
    printer with SymPy types (so that the printer safely can use SymPy-methods)."""
    from sympy.matrices.matrixbase import MatrixBase
    from sympy.core.basic import Basic

    if isinstance(arg, (Basic, MatrixBase)):
        return doprint(arg)
    elif iterable(arg):
        if isinstance(arg, list):
            left, right = "[", "]"
        elif isinstance(arg, tuple):
            left, right = "(", ",)"
            if not arg:
                return "()"
        else:
            raise NotImplementedError("unhandled type: %s, %s" % (type(arg), arg))
        return left +', '.join(_recursive_to_string(doprint, e) for e in arg) + right
    elif isinstance(arg, str):
        return arg
    else:
        return doprint(arg)

