
def pi_hex_digits(n, prec=14):
    """Returns a string containing ``prec`` (default 14) digits
    starting at the nth digit of pi in hex. Counting of digits
    starts at 0 and the decimal is not counted, so for n = 0 the
    returned value starts with 3; n = 1 corresponds to the first
    digit past the decimal point (which in hex is 2).

    Parameters
    ==========

    n : non-negative integer
    prec : non-negative integer. default = 14

    Returns
    =======

    str : Returns a string containing ``prec`` digits
          starting at the nth digit of pi in hex.
          If ``prec`` = 0, returns empty string.

    Raises
    ======

    ValueError
        If ``n`` < 0 or ``prec`` < 0.
        Or ``n`` or ``prec`` is not an integer.

    Examples
    ========

    >>> from sympy.ntheory.bbp_pi import pi_hex_digits
    >>> pi_hex_digits(0)
    '3243f6a8885a30'
    >>> pi_hex_digits(0, 3)
    '324'

    These are consistent with the following results

    >>> import math
    >>> hex(int(math.pi * 2**((14-1)*4)))
    '0x3243f6a8885a30'
    >>> hex(int(math.pi * 2**((3-1)*4)))
    '0x324'

    References
    ==========

    .. [1] http://www.numberworld.org/digits/Pi/
    """
    n, prec = as_int(n), as_int(prec)
    if n < 0:
        raise ValueError('n cannot be negative')
    if prec < 0:
        raise ValueError('prec cannot be negative')
    if prec == 0:
        return ''

    # main of implementation arrays holding formulae coefficients
    n -= 1
    a = [4, 2, 1, 1]
    j = [1, 4, 5, 6]

    #formulae
    D = _dn(n, prec)
    x = + (a[0]*_series(j[0], n, prec)
         - a[1]*_series(j[1], n, prec)
         - a[2]*_series(j[2], n, prec)
         - a[3]*_series(j[3], n, prec)) & (16**D - 1)

    s = ("%0" + "%ix" % prec) % (x // 16**(D - prec))
    return s

