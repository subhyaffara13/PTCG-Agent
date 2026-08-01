
def test_sympy__series__formal__FormalPowerSeries():
    from sympy.series.formal import fps
    assert _test_args(fps(log(1 + x), x))

