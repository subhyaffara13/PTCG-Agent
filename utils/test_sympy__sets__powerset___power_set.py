
def test_sympy__sets__powerset__PowerSet():
    from sympy.sets.powerset import PowerSet
    from sympy.core.singleton import S
    assert _test_args(PowerSet(S.EmptySet))

