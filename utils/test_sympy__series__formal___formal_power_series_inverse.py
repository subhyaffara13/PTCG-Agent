
def test_sympy__series__formal__FormalPowerSeriesInverse():
    from sympy.series.formal import fps
    f1 = fps(exp(x))
    assert _test_args(f1.inverse(x))

