
def test_erf_series():
    assert erf(x).series(x, 0, 7) == 2*x/sqrt(pi) - \
        2*x**3/3/sqrt(pi) + x**5/5/sqrt(pi) + O(x**7)

    assert erf(x).series(x, oo) == \
        -exp(-x**2)*(3/(4*x**5) - 1/(2*x**3) + 1/x + O(x**(-6), (x, oo)))/sqrt(pi) + 1
    assert erf(x**2).series(x, oo, n=8) == \
        (-1/(2*x**6) + x**(-2) + O(x**(-8), (x, oo)))*exp(-x**4)/sqrt(pi)*-1 + 1
    assert erf(sqrt(x)).series(x, oo, n=3) == (sqrt(1/x) - (1/x)**(S(3)/2)/2\
        + 3*(1/x)**(S(5)/2)/4 + O(x**(-3), (x, oo)))*exp(-x)/sqrt(pi)*-1 + 1

