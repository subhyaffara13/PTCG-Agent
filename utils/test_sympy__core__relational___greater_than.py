
def test_sympy__core__relational__GreaterThan():
    from sympy.core.relational import GreaterThan
    assert _test_args(GreaterThan(x, 2))

