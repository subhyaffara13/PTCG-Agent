
def test_expand_no_log():
    assert (
        (1 + log(x**4))**2).expand(log=False) == 1 + 2*log(x**4) + log(x**4)**2
    assert ((1 + log(x**4))*(1 + log(x**3))).expand(
        log=False) == 1 + log(x**4) + log(x**3) + log(x**4)*log(x**3)

