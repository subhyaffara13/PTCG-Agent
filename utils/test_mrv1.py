
def test_mrv1():
    assert mmrv(x, x) == {x}
    assert mmrv(x + 1/x, x) == {x}
    assert mmrv(x**2, x) == {x}
    assert mmrv(log(x), x) == {x}
    assert mmrv(exp(x), x) == {exp(x)}
    assert mmrv(exp(-x), x) == {exp(-x)}
    assert mmrv(exp(x**2), x) == {exp(x**2)}
    assert mmrv(-exp(1/x), x) == {x}
    assert mmrv(exp(x + 1/x), x) == {exp(x + 1/x)}

