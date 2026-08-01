
def to_anf(expr, deep=True):
    r"""
    Converts expr to Algebraic Normal Form (ANF).

    ANF is a canonical normal form, which means that two
    equivalent formulas will convert to the same ANF.

    A logical expression is in ANF if it has the form

    .. math:: 1 \oplus a \oplus b \oplus ab \oplus abc

    i.e. it can be:
        - purely true,
        - purely false,
        - conjunction of variables,
        - exclusive disjunction.

    The exclusive disjunction can only contain true, variables
    or conjunction of variables. No negations are permitted.

    If ``deep`` is ``False``, arguments of the boolean
    expression are considered variables, i.e. only the
    top-level expression is converted to ANF.

    Examples
    ========
    >>> from sympy.logic.boolalg import And, Or, Not, Implies, Equivalent
    >>> from sympy.logic.boolalg import to_anf
    >>> from sympy.abc import A, B, C
    >>> to_anf(Not(A))
    A ^ True
    >>> to_anf(And(Or(A, B), Not(C)))
    A ^ B ^ (A & B) ^ (A & C) ^ (B & C) ^ (A & B & C)
    >>> to_anf(Implies(Not(A), Equivalent(B, C)), deep=False)
    True ^ ~A ^ (~A & (Equivalent(B, C)))

    """
    expr = sympify(expr)

    if is_anf(expr):
        return expr
    return expr.to_anf(deep=deep)

