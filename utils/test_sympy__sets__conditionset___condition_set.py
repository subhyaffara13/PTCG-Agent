
def test_sympy__sets__conditionset__ConditionSet():
    from sympy.sets.conditionset import ConditionSet
    from sympy.core.singleton import S
    from sympy.core.symbol import Symbol
    x = Symbol('x')
    assert _test_args(ConditionSet(x, Eq(x**2, 1), S.Reals))

