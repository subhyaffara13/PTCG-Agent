
def integer_log(n, b):
    r"""
    Returns ``(e, bool)`` where e is the largest nonnegative integer
    such that :math:`|n| \geq |b^e|` and ``bool`` is True if $n = b^e$.

    Examples
    ========

    >>> from sympy import integer_log
    >>> integer_log(125, 5)
    (3, True)
    >>> integer_log(17, 9)
    (1, False)

    If the base is positive and the number negative the
    return value will always be the same except for 2:

    >>> integer_log(-4, 2)
    (2, False)
    >>> integer_log(-16, 4)
    (0, False)

    When the base is negative, the returned value
    will only be True if the parity of the exponent is
    correct for the sign of the base:

    >>> integer_log(4, -2)
    (2, True)
    >>> integer_log(8, -2)
    (3, False)
    >>> integer_log(-8, -2)
    (3, True)
    >>> integer_log(-4, -2)
    (2, False)

    See Also
    ========
    integer_nthroot
    sympy.ntheory.primetest.is_square
    sympy.ntheory.factor_.multiplicity
    sympy.ntheory.factor_.perfect_power
    """
    n = as_int(n)
    b = as_int(b)

    if b < 0:
        e, t = integer_log(abs(n), -b)
        # (-2)**3 == -8
        # (-2)**2 = 4
        t = t and e % 2 == (n < 0)
        return e, t
    if b <= 1:
        raise ValueError('base must be 2 or more')
    if n < 0:
        if b != 2:
            return 0, False
        e, t = integer_log(-n, b)
        return e, False
    if n == 0:
        raise ValueError('n cannot be 0')

    if n < b:
        return 0, n == 1
    if b == 2:
        e = n.bit_length() - 1
        return e, trailing(n) == e
    t = trailing(b)
    if 2**t == b:
        e = int(n.bit_length() - 1)//t
        n_ = 1 << (t*e)
        return e, n_ == n

    d = math.floor(math.log10(n) / math.log10(b))
    n_ = b ** d
    while n_ <= n:  # this will iterate 0, 1 or 2 times
        d += 1
        n_ *= b
    return d - (n_ > n), (n_ == n or n_//b == n)

