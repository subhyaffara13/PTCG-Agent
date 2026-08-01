
def dimension(*args):
    """ Creates a 'dimension' Attribute with (up to 7) extents.

    Examples
    ========

    >>> from sympy import fcode
    >>> from sympy.codegen.fnodes import dimension, intent_in
    >>> dim = dimension('2', ':')  # 2 rows, runtime determined number of columns
    >>> from sympy.codegen.ast import Variable, integer
    >>> arr = Variable('a', integer, attrs=[dim, intent_in])
    >>> fcode(arr.as_Declaration(), source_format='free', standard=2003)
    'integer*4, dimension(2, :), intent(in) :: a'

    """
    if len(args) > 7:
        raise ValueError("Fortran only supports up to 7 dimensional arrays")
    parameters = []
    for arg in args:
        if isinstance(arg, Extent):
            parameters.append(arg)
        elif isinstance(arg, str):
            if arg == ':':
                parameters.append(Extent())
            else:
                parameters.append(String(arg))
        elif iterable(arg):
            parameters.append(Extent(*arg))
        else:
            parameters.append(sympify(arg))
    if len(args) == 0:
        raise ValueError("Need at least one dimension")
    return Attribute('dimension', parameters)

