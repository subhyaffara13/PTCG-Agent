
def get_num_denom(c):
    r"""
    Given any argument on which :py:func:`~.is_rat` is ``True``, return the
    numerator and denominator of this number.

    See Also
    ========

    is_rat

    """
    r = QQ(c)
    return r.numerator, r.denominator

