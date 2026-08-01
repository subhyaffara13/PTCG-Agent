
def test_mrv2a():
    assert mmrv(exp(x + exp(-exp(x))), x) == {exp(-exp(x))}
    assert mmrv(exp(x + exp(-x)), x) == {exp(x + exp(-x)), exp(-x)}
    assert mmrv(exp(1/x + exp(-x)), x) == {exp(-x)}

