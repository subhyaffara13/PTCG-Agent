
def test_issue_20291():
    from sympy.sets import EmptySet, Reals
    from sympy.sets.sets import (Complement, FiniteSet, Intersection)
    a = Symbol('a')
    b = Symbol('b')
    A = FiniteSet(a, b)
    assert A.evalf(subs={a: 1, b: 2}) == FiniteSet(1.0, 2.0)
    B = FiniteSet(a-b, 1)
    assert B.evalf(subs={a: 1, b: 2}) == FiniteSet(-1.0, 1.0)

    sol = Complement(Intersection(FiniteSet(-b/2 - sqrt(b**2-4*pi)/2), Reals), FiniteSet(0))
    assert sol.evalf(subs={b: 1}) == EmptySet

