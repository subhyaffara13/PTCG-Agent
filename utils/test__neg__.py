
def test__neg__():
    assert -(x*y) == -x*y
    assert -(-x*y) == x*y
    assert -(1.*x) == -1.*x
    assert -(-1.*x) == 1.*x
    assert -(2.*x) == -2.*x
    assert -(-2.*x) == 2.*x
    with distribute(False):
        eq = -(x + y)
        assert eq.is_Mul and eq.args == (-1, x + y)
    with evaluate(False):
        eq = -(x + y)
        assert eq.is_Mul and eq.args == (-1, x + y)

