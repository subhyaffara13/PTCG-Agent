
def distribute_xor_over_and(expr):
    """
    Given a sentence ``expr`` consisting of conjunction and
    exclusive disjunctions of literals, return an
    equivalent exclusive disjunction.

    Note that the output is NOT simplified.

    Examples
    ========

    >>> from sympy.logic.boolalg import distribute_xor_over_and, And, Xor, Not
    >>> from sympy.abc import A, B, C
    >>> distribute_xor_over_and(And(Xor(Not(A), B), C))
    (B & C) ^ (C & ~A)
    """
    return _distribute((expr, Xor, And))

