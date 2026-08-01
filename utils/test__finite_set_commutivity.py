
def test_FiniteSet_commutivity():
    from sympy.sets.sets import FiniteSet
    a, b, c, x, y = symbols('a,b,c,x,y')
    s = FiniteSet(a, b, c)
    t = FiniteSet(x, y)
    variables = (x, y)
    assert {x: FiniteSet(a, c), y: b} in tuple(unify(s, t, variables=variables))

