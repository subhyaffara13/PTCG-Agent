
def test_stackoverflow_43852159():
    f = lambda x: Piecewise((1, (x >= -1) & (x <= 1)), (0, True))
    Conv = lambda x: integrate(f(x - y)*f(y), (y, -oo, +oo))
    cx = Conv(x)
    assert cx.subs(x, -1.5) == cx.subs(x, 1.5)
    assert cx.subs(x, 3) == 0
    assert piecewise_fold(f(x - y)*f(y)) == Piecewise(
        (1, (y >= -1) & (y <= 1) & (x - y >= -1) & (x - y <= 1)),
        (0, True))

