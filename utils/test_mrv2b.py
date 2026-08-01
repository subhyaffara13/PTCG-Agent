
def test_mrv2b():
    assert mmrv(exp(x + exp(-x**2)), x) == {exp(-x**2)}

