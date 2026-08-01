
def _eval_is_ge(a, b):
    if a < 2:
        return sympy.false
    raise ValueError("Symbolic SingletonInt: Relation is indeterminate")


def _eval_is_ge(a, b):  # noqa: F811
    if b <= 2:
        return sympy.true
    raise ValueError("Symbolic SingletonInt: Relation is indeterminate")


def _eval_is_ge(a, b):  # noqa: F811
    if a._val == b._val:
        if a._coeff >= b._coeff:
            return sympy.true
        else:
            return sympy.false
    raise ValueError("Symbolic SingletonInt: Relation is indeterminate")


def _eval_is_ge(lhs, rhs): # noqa:F811
    if is_ge(lhs.min, rhs.max):
        return True
    if is_lt(lhs.max, rhs.min):
        return False


def _eval_is_ge(lhs, rhs): # noqa: F811
    """
    Returns ``True`` if range of values attained by ``lhs`` AccumulationBounds
    object is less that the range of values attained by ``rhs``, where
    other may be any value of type AccumulationBounds object or extended
    real number value, ``False`` if ``rhs`` satisfies the same
    property, else an unevaluated :py:class:`~.Relational`.

    Examples
    ========

    >>> from sympy import AccumBounds, oo
    >>> AccumBounds(1, 3) >= AccumBounds(4, oo)
    False
    >>> AccumBounds(1, 4) >= AccumBounds(3, 4)
    AccumBounds(1, 4) >= AccumBounds(3, 4)
    >>> AccumBounds(1, oo) >= 1
    True
    """

    if not rhs.is_extended_real:
        raise TypeError(
            "Invalid comparison of %s %s" %
            (type(rhs), rhs))
    elif rhs.is_comparable:
        if is_ge(lhs.min, rhs):
            return True
        if is_lt(lhs.max, rhs):
            return False


def _eval_is_ge(lhs, rhs): # noqa:F811
    if not lhs.is_extended_real:
        raise TypeError(
            "Invalid comparison of %s %s" %
            (type(lhs), lhs))
    elif lhs.is_comparable:
        if is_le(rhs.max, lhs):
            return True
        if is_gt(rhs.min, lhs):
            return False


def _eval_is_ge(lhs, rhs): # noqa:F811
    if is_ge(lhs.min, rhs.max):
        return True
    if is_lt(lhs.max, rhs.min):
        return False


def _eval_is_ge(lhs, rhs):
    return None


def _eval_is_ge(lhs, rhs): # noqa:F811

    other_upper = rhs if rhs.upper is None else rhs.upper
    other_lower = rhs if rhs.lower is None else rhs.lower

    if lhs.lower is not None and (lhs.lower >= other_upper) == True:
        return True
    if lhs.upper is not None and (lhs.upper < other_lower) == True:
        return False
    return None


def _eval_is_ge(lhs, rhs): # noqa:F811

    other_upper = rhs
    other_lower = rhs

    if lhs.lower is not None and (lhs.lower >= other_upper) == True:
        return True
    if lhs.upper is not None and (lhs.upper < other_lower) == True:
        return False
    return None


def _eval_is_ge(lhs, rhs): # noqa:F811

    other_upper = lhs
    other_lower = lhs

    if rhs.upper is not None and (rhs.upper <= other_lower) == True:
        return True
    if rhs.lower is not None and (rhs.lower > other_upper) == True:
        return False
    return None

