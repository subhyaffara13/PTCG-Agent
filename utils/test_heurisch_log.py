
def test_heurisch_log():
    assert heurisch(log(x), x) == x*log(x) - x
    assert heurisch(log(3*x), x) == -x + x*log(3) + x*log(x)
    assert heurisch(log(x**2), x) in [x*log(x**2) - 2*x, 2*x*log(x) - 2*x]

