
def apply_operators(e):
    """
    Take a SymPy expression with operators and states and apply the operators.

    Examples
    ========

    >>> from sympy.physics.secondquant import apply_operators
    >>> from sympy import sympify
    >>> apply_operators(sympify(3)+4)
    7
    """
    e = e.expand()
    muls = e.atoms(Mul)
    subs_list = [(m, _apply_Mul(m)) for m in iter(muls)]
    return e.subs(subs_list)


def apply_operators(obj, ops, op):
    """
    Apply the list of operators ``ops`` to object ``obj``, substituting
    ``op`` for the generator.
    """
    res = obj
    for o in reversed(ops):
        res = o.apply(res, op)
    return res

