
def test_pmint_erf():
    f = exp(-x**2)*erf(x)/(erf(x)**3 - erf(x)**2 - erf(x) + 1)
    g = sqrt(pi)*log(erf(x) - 1)/8 - sqrt(pi)*log(erf(x) + 1)/8 - sqrt(pi)/(4*erf(x) - 4)

    assert ratsimp(heurisch(f, x)) == g

