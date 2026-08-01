
def test_sympy__series__formal__FormalPowerSeriesProduct():
    from sympy.series.formal import fps
    f1, f2 = fps(sin(x)), fps(exp(x))
    assert _test_args(f1.product(f2, x))

