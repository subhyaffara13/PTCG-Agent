
def convolution_int(a, b):
    """Return the convolution of two sequences as a list.

    The iterables must consist solely of integers.

    Parameters
    ==========

    a, b : Sequence
        The sequences for which convolution is performed.

    Explanation
    ===========

    This function performs the convolution of ``a`` and ``b`` by packing
    each into a single integer, multiplying them together, and then
    unpacking the result from the product.  The intuition behind this is
    that if we evaluate some polynomial [1]:

    .. math ::
        1156x^6 + 3808x^5 + 8440x^4 + 14856x^3 + 16164x^2 + 14040x + 8100

    at say $x = 10^5$ we obtain $1156038080844014856161641404008100$.
    Note we can read of the coefficients for each term every five digits.
    If the $x$ we chose to evaluate at is large enough, the same will hold
    for the product.

    The idea now is since big integer multiplication in libraries such
    as GMP is highly optimised, this will be reasonably fast.

    Examples
    ========

    >>> from sympy.discrete.convolutions import convolution_int

    >>> convolution_int([2, 3], [4, 5])
    [8, 22, 15]
    >>> convolution_int([1, 1, -1], [1, 1])
    [1, 2, 0, -1]

    References
    ==========

    .. [1] Fateman, Richard J.
           Can you save time in multiplying polynomials by encoding them as integers?
           University of California, Berkeley, California (2004).
           https://people.eecs.berkeley.edu/~fateman/papers/polysbyGMP.pdf
    """
    # An upper bound on the largest coefficient in p(x)q(x) is given by (1 + min(dp, dq))N(p)N(q)
    # where dp = deg(p), dq = deg(q), N(f) denotes the coefficient of largest modulus in f [1]
    B = max(abs(c) for c in a)*max(abs(c) for c in b)*(1 + min(len(a) - 1, len(b) - 1))
    x, power = MPZ(1), 0
    while x <= (2*B):  # multiply by two for negative coefficients, see [1]
        x <<= 1
        power += 1

    def to_integer(poly):
        n, mul = MPZ(0), 0
        for c in reversed(poly):
            if c and not mul: mul = -1 if c < 0 else 1
            n <<= power
            n += mul*int(c)
        return mul, n

    # Perform packing and multiplication
    (a_mul, a_packed), (b_mul, b_packed) = to_integer(a), to_integer(b)
    result = a_packed * b_packed

    # Perform unpacking
    mul = a_mul * b_mul
    mask, half, borrow, poly = x - 1, x >> 1, 0, []
    while result or borrow:
        coeff = (result & mask) + borrow
        result >>= power
        borrow = coeff >= half
        poly.append(mul * int(coeff if coeff < half else coeff - x))
    return poly or [0]

