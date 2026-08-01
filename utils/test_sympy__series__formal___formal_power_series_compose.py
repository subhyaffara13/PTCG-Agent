
def test_sympy__series__formal__FormalPowerSeriesCompose():
    from sympy.series.formal import fps
    f1, f2 = fps(exp(x)), fps(sin(x))
    assert _test_args(f1.compose(f2, x))

