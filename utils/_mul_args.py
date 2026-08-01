
def _mul_args(f):
    """
    Return a list ``L`` such that ``Mul(*L) == f``.

    If ``f`` is not a ``Mul`` or ``Pow``, ``L=[f]``.
    If ``f=g**n`` for an integer ``n``, ``L=[g]*n``.
    If ``f`` is a ``Mul``, ``L`` comes from applying ``_mul_args`` to all factors of ``f``.
    """
    args = Mul.make_args(f)
    gs = []
    for g in args:
        if g.is_Pow and g.exp.is_Integer:
            n = g.exp
            base = g.base
            if n < 0:
                n = -n
                base = 1/base
            gs += [base]*n
        else:
            gs.append(g)
    return gs

