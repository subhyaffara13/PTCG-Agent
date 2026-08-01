
def test_sympy__series__limits__Limit():
    from sympy.series.limits import Limit
    assert _test_args(Limit(x, x, 0, dir='-'))

