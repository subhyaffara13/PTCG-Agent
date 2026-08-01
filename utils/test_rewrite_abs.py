
def test_rewrite_abs():
    # https://github.com/sympy/sympy/issues/27323
    x = Symbol('x')
    assert sign(x).rewrite(abs) == sign(x).rewrite(Abs)
    assert sign(x).rewrite(abs) == Piecewise((0, Eq(x, 0)), (x / Abs(x), True))

