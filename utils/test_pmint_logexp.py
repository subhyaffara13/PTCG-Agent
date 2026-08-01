
def test_pmint_logexp():
    f = (1 + x + x*exp(x))*(x + log(x) + exp(x) - 1)/(x + log(x) + exp(x))**2/x
    g = log(x + exp(x) + log(x)) + 1/(x + exp(x) + log(x))

    assert ratsimp(heurisch(f, x)) == g

