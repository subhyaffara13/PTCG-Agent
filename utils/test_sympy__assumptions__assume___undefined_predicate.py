
def test_sympy__assumptions__assume__UndefinedPredicate():
    from sympy.assumptions.assume import Predicate
    assert _test_args(Predicate("test"))

