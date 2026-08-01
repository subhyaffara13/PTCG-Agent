
def test_issue_6799():
    r, x, phi = map(Symbol, 'r x phi'.split())
    n = Symbol('n', integer=True, positive=True)

    integrand = (cos(n*(x-phi))*cos(n*x))
    limits = (x, -pi, pi)
    assert manualintegrate(integrand, x) == \
        ((n*x/2 + sin(2*n*x)/4)*cos(n*phi) - sin(n*phi)*cos(n*x)**2/2)/n
    assert r * integrate(integrand, limits).trigsimp() / pi == r * cos(n * phi)
    assert not integrate(integrand, limits).has(Dummy)

