
def test_mrv2c():
    assert mmrv(
        exp(-x + 1/x**2) - exp(x + 1/x), x) == {exp(x + 1/x), exp(1/x**2 - x)}

