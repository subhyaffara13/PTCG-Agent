
def test_heurisch_mixed():
    assert heurisch(sin(x)*exp(x), x) == exp(x)*sin(x)/2 - exp(x)*cos(x)/2
    assert heurisch(sin(x/sqrt(-x)), x) == 2*x*cos(x/sqrt(-x))/sqrt(-x) - 2*sin(x/sqrt(-x))

