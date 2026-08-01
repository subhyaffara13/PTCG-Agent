
def is_perfect(n):
    """Returns True if ``n`` is a perfect number, else False.

    A perfect number is equal to the sum of its positive, proper divisors.

    Examples
    ========

    >>> from sympy.functions.combinatorial.numbers import divisor_sigma
    >>> from sympy.ntheory.factor_ import is_perfect, divisors
    >>> is_perfect(20)
    False
    >>> is_perfect(6)
    True
    >>> 6 == divisor_sigma(6) - 6 == sum(divisors(6)[:-1])
    True

    References
    ==========

    .. [1] https://mathworld.wolfram.com/PerfectNumber.html
    .. [2] https://en.wikipedia.org/wiki/Perfect_number

    """
    n = as_int(n)
    if n < 1:
        return False
    if n % 2 == 0:
        m = (n.bit_length() + 1) >> 1
        if (1 << (m - 1)) * ((1 << m) - 1) != n:
            # Even perfect numbers must be of the form `2^{m-1}(2^m-1)`
            return False
        return m in MERSENNE_PRIME_EXPONENTS or is_mersenne_prime(2**m - 1)

    # n is an odd integer
    if n < 10**2000:  # https://www.lirmm.fr/~ochem/opn/
        return False
    if n % 105 == 0:  # not divis by 105
        return False
    if all(n % m != r for m, r in [(12, 1), (468, 117), (324, 81)]):
        return False
    # there are many criteria that the factor structure of n
    # must meet; since we will have to factor it to test the
    # structure we will have the factors and can then check
    # to see whether it is a perfect number or not. So we
    # skip the structure checks and go straight to the final
    # test below.
    result = abundance(n) == 0
    if result:
        raise ValueError(filldedent('''In 1888, Sylvester stated: "
            ...a prolonged meditation on the subject has satisfied
            me that the existence of any one such [odd perfect number]
            -- its escape, so to say, from the complex web of conditions
            which hem it in on all sides -- would be little short of a
            miracle." I guess SymPy just found that miracle and it
            factors like this: %s''' % factorint(n)))
    return result

