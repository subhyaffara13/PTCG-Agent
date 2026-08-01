
def _eval_is_le(lhs, rhs): # noqa:F811
    if is_le(lhs.max, rhs.min):
        return True
    if is_gt(lhs.min, rhs.max):
        return False


def _eval_is_le(lhs, rhs): # noqa: F811

    """
    Returns ``True `` if range of values attained by ``lhs`` AccumulationBounds
    object is greater than the range of values attained by ``rhs``,
    where ``rhs`` may be any value of type AccumulationBounds object or
    extended real number value, ``False`` if ``rhs`` satisfies
    the same property, else an unevaluated :py:class:`~.Relational`.

    Examples
    ========

    >>> from sympy import AccumBounds, oo
    >>> AccumBounds(1, 3) > AccumBounds(4, oo)
    False
    >>> AccumBounds(1, 4) > AccumBounds(3, 4)
    AccumBounds(1, 4) > AccumBounds(3, 4)
    >>> AccumBounds(1, oo) > -1
    True

    """
    if not rhs.is_extended_real:
            raise TypeError(
                "Invalid comparison of %s %s" %
                (type(rhs), rhs))
    elif rhs.is_comparable:
        if is_le(lhs.max, rhs):
            return True
        if is_gt(lhs.min, rhs):
            return False

