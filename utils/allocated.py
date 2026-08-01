
def allocated(array):
    """ Creates an AST node for a function call to Fortran's "allocated(...)"

    Examples
    ========

    >>> from sympy import fcode
    >>> from sympy.codegen.fnodes import allocated
    >>> alloc = allocated('x')
    >>> fcode(alloc, source_format='free')
    'allocated(x)'

    """
    return FunctionCall('allocated', [_printable(array)])

