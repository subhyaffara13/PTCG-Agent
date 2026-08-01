
def disjuncts(expr):
    """Return a list of the disjuncts in ``expr``.

    Examples
    ========

    >>> from sympy.logic.boolalg import disjuncts
    >>> from sympy.abc import A, B
    >>> disjuncts(A | B)
    frozenset({A, B})
    >>> disjuncts(A & B)
    frozenset({A & B})

    """
    return Or.make_args(expr)

