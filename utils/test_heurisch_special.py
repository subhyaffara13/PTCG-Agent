
def test_heurisch_special():
    assert heurisch(erf(x), x) == x*erf(x) + exp(-x**2)/sqrt(pi)
    assert heurisch(exp(-x**2)*erf(x), x) == sqrt(pi)*erf(x)**2 / 4

