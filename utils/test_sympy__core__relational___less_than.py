
def test_sympy__core__relational__LessThan():
    from sympy.core.relational import LessThan
    assert _test_args(LessThan(x, 2))

