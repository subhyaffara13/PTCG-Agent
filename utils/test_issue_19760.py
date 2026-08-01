
def test_issue_19760():
    e = 1/(sqrt(1 + sqrt(2)) - sqrt(2)*sqrt(1 + sqrt(2))) + 1
    mp_expected = x**4 - 4*x**3 + 4*x**2 - 2

    for comp in (True, False):
        mp = Poly(minimal_polynomial(e, compose=comp))
        assert mp(x) == mp_expected, "minimal_polynomial(e, compose=%s) = %s; %s expected" % (comp, mp(x), mp_expected)

