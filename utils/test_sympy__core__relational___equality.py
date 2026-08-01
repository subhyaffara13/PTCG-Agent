
def test_sympy__core__relational__Equality():
    from sympy.core.relational import Equality
    assert _test_args(Equality(x, 2))

