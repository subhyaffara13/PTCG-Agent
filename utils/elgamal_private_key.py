
def elgamal_private_key(digit=10, seed=None):
    r"""
    Return three number tuple as private key.

    Explanation
    ===========

    Elgamal encryption is based on the mathematical problem
    called the Discrete Logarithm Problem (DLP). For example,

    `a^{b} \equiv c \pmod p`

    In general, if ``a`` and ``b`` are known, ``ct`` is easily
    calculated. If ``b`` is unknown, it is hard to use
    ``a`` and ``ct`` to get ``b``.

    Parameters
    ==========

    digit : int
        Minimum number of binary digits for key.

    Returns
    =======

    tuple : (p, r, d)
        p = prime number.

        r = primitive root.

        d = random number.

    Notes
    =====

    For testing purposes, the ``seed`` parameter may be set to control
    the output of this routine. See sympy.core.random._randrange.

    Examples
    ========

    >>> from sympy.crypto.crypto import elgamal_private_key
    >>> from sympy.ntheory import is_primitive_root, isprime
    >>> a, b, _ = elgamal_private_key()
    >>> isprime(a)
    True
    >>> is_primitive_root(b, a)
    True

    """
    randrange = _randrange(seed)
    p = nextprime(2**digit)
    return p, primitive_root(p), randrange(2, p)

