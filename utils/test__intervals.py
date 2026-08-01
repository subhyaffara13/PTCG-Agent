
def test__intervals():
    assert Piecewise((x + 2, Eq(x, 3)))._intervals(x) == (True, [])
    assert Piecewise(
        (1, x > x + 1),
        (Piecewise((1, x < x + 1)), 2*x < 2*x + 1),
        (1, True))._intervals(x) == (True, [(-oo, oo, 1, 1)])
    assert Piecewise((1, Ne(x, I)), (0, True))._intervals(x) == (True,
        [(-oo, oo, 1, 0)])
    assert Piecewise((-cos(x), sin(x) >= 0), (cos(x), True)
        )._intervals(x) == (True,
        [(0, pi, -cos(x), 0), (-oo, oo, cos(x), 1)])
    # the following tests that duplicates are removed and that non-Eq
    # generated zero-width intervals are removed
    assert Piecewise((1, Abs(x**(-2)) > 1), (0, True)
        )._intervals(x) == (True,
        [(-1, 0, 1, 0), (0, 1, 1, 0), (-oo, oo, 0, 1)])

