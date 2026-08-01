
def test_besselk_leading_term():
    assert besselk(0, x).as_leading_term(x) == -log(x) - S.EulerGamma + log(2)
    assert besselk(1, sin(x)).as_leading_term(x) == 1/x
    assert besselk(1, 2*sqrt(x)).as_leading_term(x) == 1/(2*sqrt(x))
    assert besselk(S(5)/3, x).as_leading_term(x) == 2**(S(2)/3)*gamma(S(5)/3)/x**(S(5)/3)
    assert besselk(S(2)/3, x).as_leading_term(x) == besselk(-S(2)/3, x).as_leading_term(x)
    assert besselk(1,cos(x)).as_leading_term(x) == besselk(1,1)
    assert besselk(3,1/x).as_leading_term(x) == sqrt(pi)*exp(-(1/x))/sqrt(2/x)
    assert besselk(3,1/sin(x)).as_leading_term(x) == sqrt(pi)*exp(-(1/x))/sqrt(2/x)

    nz = Symbol("nz", nonzero=True)
    assert besselk(nz, x).as_leading_term(x).subs({nz:S(5)/7}) == besselk(S(5)/7, x).series(x).as_leading_term(x)
    assert besselk(nz, x).as_leading_term(x).subs({nz:S(-15)/7}) == besselk(S(-15)/7, x).series(x).as_leading_term(x)
    assert besselk(nz, x).as_leading_term(x).subs({nz:3}) == besselk(3, x).series(x).as_leading_term(x)
    assert besselk(nz, x).as_leading_term(x).subs({nz:-2}) == besselk(-2, x).series(x).as_leading_term(x)

