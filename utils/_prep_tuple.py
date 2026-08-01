
def _prep_tuple(v):
    """
    Turn an iterable argument *v* into a tuple and unpolarify, since both
    hypergeometric and meijer g-functions are unbranched in their parameters.

    Examples
    ========

    >>> from sympy.functions.special.hyper import _prep_tuple
    >>> _prep_tuple([1, 2, 3])
    (1, 2, 3)
    >>> _prep_tuple((4, 5))
    (4, 5)
    >>> _prep_tuple((7, 8, 9))
    (7, 8, 9)

    """
    return TupleArg(*[unpolarify(x) for x in v])

