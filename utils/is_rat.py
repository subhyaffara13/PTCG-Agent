
def is_rat(c):
    r"""
    Test whether an argument is of an acceptable type to be used as a rational
    number.

    Explanation
    ===========

    Returns ``True`` on any argument of type ``int``, :ref:`ZZ`, or :ref:`QQ`.

    See Also
    ========

    is_int

    """
    # ``c in QQ`` is too accepting (e.g. ``3.14 in QQ`` is ``True``),
    # ``QQ.of_type(c)`` is too demanding (e.g. ``QQ.of_type(3)`` is ``False``).
    #
    # Meanwhile, if gmpy2 is installed then ``ZZ.of_type()`` accepts only
    # ``mpz``, not ``int``, so we need another clause to ensure ``int`` is
    # accepted.
    return isinstance(c, int) or ZZ.of_type(c) or QQ.of_type(c)

