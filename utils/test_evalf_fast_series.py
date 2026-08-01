
def test_evalf_fast_series():
    # Euler transformed series for sqrt(1+x)
    assert NS(Sum(
        fac(2*n + 1)/fac(n)**2/2**(3*n + 1), (n, 0, oo)), 100) == NS(sqrt(2), 100)

    # Some series for exp(1)
    estr = NS(E, 100)
    assert NS(Sum(1/fac(n), (n, 0, oo)), 100) == estr
    assert NS(1/Sum((1 - 2*n)/fac(2*n), (n, 0, oo)), 100) == estr
    assert NS(Sum((2*n + 1)/fac(2*n), (n, 0, oo)), 100) == estr
    assert NS(Sum((4*n + 3)/2**(2*n + 1)/fac(2*n + 1), (n, 0, oo))**2, 100) == estr

    pistr = NS(pi, 100)
    # Ramanujan series for pi
    assert NS(9801/sqrt(8)/Sum(fac(
        4*n)*(1103 + 26390*n)/fac(n)**4/396**(4*n), (n, 0, oo)), 100) == pistr
    assert NS(1/Sum(
        binomial(2*n, n)**3 * (42*n + 5)/2**(12*n + 4), (n, 0, oo)), 100) == pistr
    # Machin's formula for pi
    assert NS(16*Sum((-1)**n/(2*n + 1)/5**(2*n + 1), (n, 0, oo)) -
        4*Sum((-1)**n/(2*n + 1)/239**(2*n + 1), (n, 0, oo)), 100) == pistr

    # Apery's constant
    astr = NS(zeta(3), 100)
    P = 126392*n**5 + 412708*n**4 + 531578*n**3 + 336367*n**2 + 104000* \
        n + 12463
    assert NS(Sum((-1)**n * P / 24 * (fac(2*n + 1)*fac(2*n)*fac(
        n))**3 / fac(3*n + 2) / fac(4*n + 3)**3, (n, 0, oo)), 100) == astr
    assert NS(Sum((-1)**n * (205*n**2 + 250*n + 77)/64 * fac(n)**10 /
              fac(2*n + 1)**5, (n, 0, oo)), 100) == astr

