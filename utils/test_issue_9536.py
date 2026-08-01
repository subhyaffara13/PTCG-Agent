
def test_issue_9536():
    from sympy.functions.elementary.exponential import log
    a = Symbol('a', real=True)
    assert FiniteSet(log(a)).intersect(S.Reals) == Intersection(S.Reals, FiniteSet(log(a)))

