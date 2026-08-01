
def lbound(array, dim=None, kind=None):
    """ Creates an AST node for a function call to Fortran's "lbound(...)"

    Parameters
    ==========

    array : Symbol or String
    dim : expr
    kind : expr

    Examples
    ========

    >>> from sympy import fcode
    >>> from sympy.codegen.fnodes import lbound
    >>> lb = lbound('arr', dim=2)
    >>> fcode(lb, source_format='free')
    'lbound(arr, 2)'

    """
    return FunctionCall(
        'lbound',
        [_printable(array)] +
        ([_printable(dim)] if dim else []) +
        ([_printable(kind)] if kind else [])
    )

