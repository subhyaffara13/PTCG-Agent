
def test_match_deriv_bug1():
    n = Function('n')
    l = Function('l')

    x = Symbol('x')
    p = Wild('p')

    e = diff(l(x), x)/x - diff(diff(n(x), x), x)/2 - \
        diff(n(x), x)**2/4 + diff(n(x), x)*diff(l(x), x)/4
    e = e.subs(n(x), -l(x)).doit()
    t = x*exp(-l(x))
    t2 = t.diff(x, x)/t
    assert e.match( (p*t2).expand() ) == {p: Rational(-1, 2)}

