
def test_sympy__series__formal__Coeff():
    from sympy.series.formal import fps
    assert _test_args(fps(x**2 + x + 1, x))

