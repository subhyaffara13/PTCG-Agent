
def unbranched_argument(arg):
    '''
    Returns periodic argument of arg with period as infinity.

    Examples
    ========

    >>> from sympy import exp_polar, unbranched_argument
    >>> from sympy import I, pi
    >>> unbranched_argument(exp_polar(15*I*pi))
    15*pi
    >>> unbranched_argument(exp_polar(7*I*pi))
    7*pi

    See also
    ========

    periodic_argument
    '''
    return periodic_argument(arg, oo)

