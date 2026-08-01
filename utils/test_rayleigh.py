
def test_rayleigh():
    sigma = Symbol("sigma", positive=True)

    X = Rayleigh('x', sigma)

    #Tests characteristic_function
    assert characteristic_function(X)(x) == (-sqrt(2)*sqrt(pi)*sigma*x*(erfi(sqrt(2)*sigma*x/2) - I)*exp(-sigma**2*x**2/2)/2 + 1)

    assert density(X)(x) ==  x*exp(-x**2/(2*sigma**2))/sigma**2
    assert E(X) == sqrt(2)*sqrt(pi)*sigma/2
    assert variance(X) == -pi*sigma**2/2 + 2*sigma**2
    assert cdf(X)(x) == 1 - exp(-x**2/(2*sigma**2))
    assert diff(cdf(X)(x), x) == density(X)(x)

