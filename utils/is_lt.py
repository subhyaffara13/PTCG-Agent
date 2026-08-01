
def is_lt(lhs, rhs, assumptions=None):
    """Fuzzy bool for lhs is strictly less than rhs.

    See the docstring for :func:`~.is_ge` for more.
    """
    return fuzzy_not(is_ge(lhs, rhs, assumptions))

