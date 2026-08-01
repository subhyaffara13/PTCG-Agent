
def test_sympy__core__relational__StrictGreaterThan():
    from sympy.core.relational import StrictGreaterThan
    assert _test_args(StrictGreaterThan(x, 2))

