
def test_piecewise_interval():
    p1 = Piecewise((x, Interval(0, 1).contains(x)), (0, True))
    assert p1.subs(x, -0.5) == 0
    assert p1.subs(x, 0.5) == 0.5
    assert p1.diff(x) == Piecewise((1, Interval(0, 1).contains(x)), (0, True))
    assert integrate(p1, x) == Piecewise(
        (0, x <= 0),
        (x**2/2, x <= 1),
        (S.Half, True))

