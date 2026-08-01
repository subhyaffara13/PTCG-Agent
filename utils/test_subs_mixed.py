
def test_subs_mixed():
    a, b, c, d, K = symbols('a b c d K', commutative=True)
    w, x, y, z, L = symbols('w x y z L', commutative=False)
    R, S, T, U = symbols('R S T U', cls=Wild)

    assert (a*x*y).subs(x*y, L) == a*L
    assert (a*b*x*y*x).subs(x*y, L) == a*b*L*x
    assert (R*x*y*exp(x*y)).subs(x*y, L) == R*L*exp(L)
    assert (a*x*y*y*x - x*y*z*exp(a*b)).subs(x*y, L) == a*L*y*x - L*z*exp(a*b)
    e = c*y*x*y*x**(R*S - a*b) - T*(a*R*b*S)
    assert e.subs(x*y, L).subs(a*b, K).subs(R*S, U) == \
        c*y*L*x**(U - K) - T*(U*K)

