
def test_sympy__core__relational__Unequality():
    from sympy.core.relational import Unequality
    assert _test_args(Unequality(x, 2))

