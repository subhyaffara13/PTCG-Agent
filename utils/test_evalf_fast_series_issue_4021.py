
def test_evalf_fast_series_issue_4021():
    # Catalan's constant
    assert NS(Sum((-1)**(n - 1)*2**(8*n)*(40*n**2 - 24*n + 3)*fac(2*n)**3*
        fac(n)**2/n**3/(2*n - 1)/fac(4*n)**2, (n, 1, oo))/64, 100) == \
        NS(Catalan, 100)
    astr = NS(zeta(3), 100)
    assert NS(5*Sum(
        (-1)**(n - 1)*fac(n)**2 / n**3 / fac(2*n), (n, 1, oo))/2, 100) == astr
    assert NS(Sum((-1)**(n - 1)*(56*n**2 - 32*n + 5) / (2*n - 1)**2 * fac(n - 1)
              **3 / fac(3*n), (n, 1, oo))/4, 100) == astr

