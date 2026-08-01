
def test_besselk_frac_order_series():
    assert besselk(S(5)/3, x).series(x, n=2) == 2**(S(2)/3)*gamma(S(5)/3)/x**(S(5)/3) - \
        3*gamma(S(5)/3)*x**(S(1)/3)/(4*2**(S(1)/3)) + \
            gamma(-S(5)/3)*x**(S(5)/3)/(4*2**(S(2)/3)) + O(x**2)
    assert besselk(S(1)/2, x).series(x, n=2) == sqrt(pi/2)/sqrt(x) - \
        sqrt(pi*x/2) + x**(S(3)/2)*sqrt(pi/2)/2 + O(x**2)
    assert besselk(S(1)/2, sqrt(x)).series(x, n=2) == sqrt(pi/2)/x**(S(1)/4) - \
        sqrt(pi/2)*x**(S(1)/4) + sqrt(pi/2)*x**(S(3)/4)/2 - \
            sqrt(pi/2)*x**(S(5)/4)/6 + sqrt(pi/2)*x**(S(7)/4)/24 + O(x**2)
    assert besselk(S(1)/2, x**2).series(x, n=2) == sqrt(pi/2)/x \
        - sqrt(pi/2)*x + O(x**2)
    assert besselk(-S(1)/2, x).series(x) == besselk(S(1)/2, x).series(x)
    assert besselk(-S(7)/6, x).series(x) == besselk(S(7)/6, x).series(x)

