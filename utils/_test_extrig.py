
def _test_extrig(f, i, e):
    from sympy.core.function import expand_trig
    assert unchanged(f, i)
    assert expand_trig(f(i)) == f(i)
    # testing directly instead of with .expand(trig=True)
    # because the other expansions undo the unevaluated Mul
    assert expand_trig(f(Mul(i, 1, evaluate=False))) == e
    assert abs(f(i) - e).n() < 1e-10

