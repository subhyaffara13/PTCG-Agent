
def test_besselk_series():
    const = log(2) - S.EulerGamma - log(x)
    assert besselk(0, x).series(x, n=4) == const + \
        x**2*(-log(x)/4 - S.EulerGamma/4 + log(2)/4 + S(1)/4) + O(x**4*log(x))
    assert besselk(1, x).series(x, n=4) == 1/x + x*(log(x)/2 - log(2)/2 - \
        S(1)/4 + S.EulerGamma/2) + x**3*(log(x)/16 - S(5)/64 - log(2)/16 + \
        S.EulerGamma/16) + O(x**4*log(x))
    assert besselk(2, x).series(x, n=4) == 2/x**2 - S(1)/2 + x**2*(-log(x)/8 - \
        S.EulerGamma/8 + log(2)/8 + S(3)/32) + O(x**4*log(x))
    assert besselk(2, x).series(x, n=1) == 2/x**2 - S(1)/2 + O(x) #edge case for series truncation
    assert besselk(0, x**(1.1)).series(x, n=4) == log(2) - S.EulerGamma - \
        1.1*log(x) + x**2.2*(-0.275*log(x) - S.EulerGamma/4 + \
        log(2)/4 + S(1)/4) + O(x**4*log(x))
    assert besselk(0, x**2 + x).series(x, n=4) == const + \
        (2 - 2*S.EulerGamma)*(x**3/4 + x**2/8) - x + x**2*(-log(x)/4 + \
        log(2)/4 + S(1)/2) + x**3*(-log(x)/2 - S(7)/12 + log(2)/2) + O(x**4*log(x))
    assert besselk(0, x/(1 - x)).series(x, n=3) == const - x + x**2*(-log(x)/4 - \
        S(1)/4 - S.EulerGamma/4 + log(2)/4) + O(x**3*log(x))
    assert besselk(0, log(1 + x)).series(x, n=3) == const + x/2 + \
        x**2*(-log(x)/4 - S.EulerGamma/4 + S(1)/24 + log(2)/4) + O(x**3*log(x))
    assert besselk(1, 2*sqrt(x)).series(x, n=3) == 1/(2*sqrt(x)) + \
        sqrt(x)*(log(x)/2 - S(1)/2 + S.EulerGamma) + x**(S(3)/2)*(log(x)/4 - S(5)/8 + \
        S.EulerGamma/2) + x**(S(5)/2)*(log(x)/24 - S(5)/36 + S.EulerGamma/12) + O(x**3*log(x))
    assert besselk(-2, sin(x)).series(x, n=4) == besselk(2, sin(x)).series(x, n=4)
    assert besselk(2, x**2).series(x, n=2) == 2/x**4 - S(1)/2 + O(x**2) #edge case for series truncation
    assert besselk(2, x**2).series(x, n=6) == 2/x**4 - S(1)/2 + x**4*(-log(x)/4 - S.EulerGamma/8 + log(2)/8 + S(3)/32) + O(x**6*log(x))
    assert (x**2*besselk(2, x)).series(x, n=2) == 2 + O(x**2)

    #test for aseries
    assert besselk(0,x).series(x, oo, n=4) == sqrt(2)*sqrt(pi)*(sqrt(1/x) + (1/x)**(S(3)/2)/8 - \
            3*(1/x)**(S(5)/2)/128 + 15*(1/x)**(S(7)/2)/1024 + O((1/x)**(S(9)/2), (x, oo)))*exp(-x)/2
    assert besselk(0,x).series(x, -oo, n=4) == sqrt(2)*sqrt(pi)*(-I*sqrt(-1/x) + I*(-1/x)**(S(3)/2)/8 + \
            3*I*(-1/x)**(S(5)/2)/128 + 15*I*(-1/x)**(S(7)/2)/1024 + O((-1/x)**(S(9)/2), (x, -oo)))*exp(-x)/2

