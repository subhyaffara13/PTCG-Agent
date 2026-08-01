
def is_gt(lhs, rhs, assumptions=None):
    """Fuzzy bool for lhs is strictly greater than rhs.

    See the docstring for :func:`~.is_ge` for more.
    """
    return fuzzy_not(is_le(lhs, rhs, assumptions))

