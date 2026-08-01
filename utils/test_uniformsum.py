
def test_uniformsum():
    n = Symbol("n", integer=True)
    _k = Dummy("k")
    x = Symbol("x")

    X = UniformSum('x', n)
    res = Sum((-1)**_k*(-_k + x)**(n - 1)*binomial(n, _k), (_k, 0, floor(x)))/factorial(n - 1)
    assert density(X)(x).dummy_eq(res)

    #Tests set functions
    assert X.pspace.domain.set == Interval(0, n)

    #Tests the characteristic_function
    assert characteristic_function(X)(x) == (-I*(exp(I*x) - 1)/x)**n

    #Tests the moment_generating_function
    assert moment_generating_function(X)(x) == ((exp(x) - 1)/x)**n

