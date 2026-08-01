
def test_issue_5651():
    a, b, c, K = symbols('a b c K', commutative=True)
    assert (a/(b*c)).subs(b*c, K) == a/K
    assert (a/(b**2*c**3)).subs(b*c, K) == a/(c*K**2)
    assert (1/(x*y)).subs(x*y, 2) == S.Half
    assert ((1 + x*y)/(x*y)).subs(x*y, 1) == 2
    assert (x*y*z).subs(x*y, 2) == 2*z
    assert ((1 + x*y)/(x*y)/z).subs(x*y, 1) == 2/z

