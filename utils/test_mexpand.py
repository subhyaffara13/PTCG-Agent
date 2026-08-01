
def test_mexpand():
    from sympy.abc import x
    assert _mexpand(None) is None
    assert _mexpand(1) is S.One
    assert _mexpand(x*(x + 1)**2) == (x*(x + 1)**2).expand()

