
def test_sympy__core__relational__StrictLessThan():
    from sympy.core.relational import StrictLessThan
    assert _test_args(StrictLessThan(x, 2))

