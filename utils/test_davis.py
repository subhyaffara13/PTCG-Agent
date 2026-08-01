
def test_davis():
    b = Symbol("b", positive=True)
    n = Symbol("n", positive=True)
    mu = Symbol("mu", positive=True)

    X = Davis('x', b, n, mu)
    dividend = b**n*(x - mu)**(-1-n)
    divisor = (exp(b/(x-mu))-1)*(gamma(n)*zeta(n))
    assert density(X)(x) == dividend/divisor

