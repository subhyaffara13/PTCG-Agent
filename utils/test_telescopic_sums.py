
def test_telescopic_sums():
    #checks also input 2 of comment 1 issue 4127
    assert Sum(1/k - 1/(k + 1), (k, 1, n)).doit() == 1 - 1/(1 + n)
    assert Sum(
        f(k) - f(k + 2), (k, m, n)).doit() == -f(1 + n) - f(2 + n) + f(m) + f(1 + m)
    assert Sum(cos(k) - cos(k + 3), (k, 1, n)).doit() == -cos(1 + n) - \
        cos(2 + n) - cos(3 + n) + cos(1) + cos(2) + cos(3)

    # dummy variable shouldn't matter
    assert telescopic(1/m, -m/(1 + m), (m, n - 1, n)) == \
        telescopic(1/k, -k/(1 + k), (k, n - 1, n))

    assert Sum(1/x/(x - 1), (x, a, b)).doit() == 1/(a - 1) - 1/b
    eq = 1/((5*n + 2)*(5*(n + 1) + 2))
    assert Sum(eq, (n, 0, oo)).doit() == S(1)/10
    nz = symbols('nz', nonzero=True)
    v = Sum(eq.subs(5, nz), (n, 0, oo)).doit()
    assert v.subs(nz, 5).simplify() == S(1)/10
    # check that apart is being used in non-symbolic case
    s = Sum(eq, (n, 0, k)).doit()
    v = Sum(eq, (n, 0, 10**100)).doit()
    assert v == s.subs(k, 10**100)

