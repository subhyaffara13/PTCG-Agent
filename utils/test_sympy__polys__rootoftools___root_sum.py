
def test_sympy__polys__rootoftools__RootSum():
    from sympy.polys.rootoftools import RootSum
    assert _test_args(RootSum(x**3 + x + 1, sin))

