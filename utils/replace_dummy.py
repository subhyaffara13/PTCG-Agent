
def replace_dummy(expr, sym):
    from sympy.core.symbol import Dummy
    dum = expr.atoms(Dummy)
    if not dum:
        return expr
    assert len(dum) == 1
    return expr.xreplace({dum.pop(): sym})

