
def test_mrv3():
    assert mmrv(exp(x**2) + x*exp(x) + log(x)**x/x, x) == {exp(x**2)}
    assert mmrv(
        exp(x)*(exp(1/x + exp(-x)) - exp(1/x)), x) == {exp(x), exp(-x)}
    assert mmrv(log(
        x**2 + 2*exp(exp(3*x**3*log(x)))), x) == {exp(exp(3*x**3*log(x)))}
    assert mmrv(log(x - log(x))/log(x), x) == {x}
    assert mmrv(
        (exp(1/x - exp(-x)) - exp(1/x))*exp(x), x) == {exp(x), exp(-x)}
    assert mmrv(
        1/exp(-x + exp(-x)) - exp(x), x) == {exp(x), exp(-x), exp(x - exp(-x))}
    assert mmrv(log(log(x*exp(x*exp(x)) + 1)), x) == {exp(x*exp(x))}
    assert mmrv(exp(exp(log(log(x) + 1/x))), x) == {x}

