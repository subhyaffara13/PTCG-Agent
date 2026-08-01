
def test_holes():
    nan = Undefined
    assert Piecewise((1, x < 2)).integrate(x) == Piecewise(
        (x, x < 2), (nan, True))
    assert Piecewise((1, And(x > 1, x < 2))).integrate(x) == Piecewise(
        (nan, x < 1), (x, x < 2), (nan, True))
    assert Piecewise((1, And(x > 1, x < 2))).integrate((x, 0, 3)) is nan
    assert Piecewise((1, And(x > 0, x < 4))).integrate((x, 1, 3)) == 2

    # this also tests that the integrate method is used on non-Piecwise
    # arguments in _eval_integral
    A, B = symbols("A B")
    a, b = symbols('a b', real=True)
    assert Piecewise((A, And(x < 0, a < 1)), (B, Or(x < 1, a > 2))
        ).integrate(x) == Piecewise(
        (B*x, (a > 2)),
        (Piecewise((A*x, x < 0), (B*x, x < 1), (nan, True)), a < 1),
        (Piecewise((B*x, x < 1), (nan, True)), True))

