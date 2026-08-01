
def test_subs_commutative():
    a, b, c, d, K = symbols('a b c d K', commutative=True)

    assert (a*b).subs(a*b, K) == K
    assert (a*b*a*b).subs(a*b, K) == K**2
    assert (a*a*b*b).subs(a*b, K) == K**2
    assert (a*b*c*d).subs(a*b*c, K) == d*K
    assert (a*b**c).subs(a, K) == K*b**c
    assert (a*b**c).subs(b, K) == a*K**c
    assert (a*b**c).subs(c, K) == a*b**K
    assert (a*b*c*b*a).subs(a*b, K) == c*K**2
    assert (a**3*b**2*a).subs(a*b, K) == a**2*K**2

