
def test_Sample():
    X = Die('X', 6)
    Y = Normal('Y', 0, 1)
    z = Symbol('z', integer=True)

    scipy = import_module('scipy')
    if not scipy:
        skip('Scipy is not installed. Abort tests')
    assert sample(X) in [1, 2, 3, 4, 5, 6]
    assert isinstance(sample(X + Y), float)

    assert P(X + Y > 0, Y < 0, numsamples=10).is_number
    assert E(X + Y, numsamples=10).is_number
    assert E(X**2 + Y, numsamples=10).is_number
    assert E((X + Y)**2, numsamples=10).is_number
    assert variance(X + Y, numsamples=10).is_number

    raises(TypeError, lambda: P(Y > z, numsamples=5))

    assert P(sin(Y) <= 1, numsamples=10) == 1.0
    assert P(sin(Y) <= 1, cos(Y) < 1, numsamples=10) == 1.0

    assert all(i in range(1, 7) for i in density(X, numsamples=10))
    assert all(i in range(4, 7) for i in density(X, X>3, numsamples=10))

    numpy = import_module('numpy')
    if not numpy:
        skip('Numpy is not installed. Abort tests')
    #Test Issue #21563: Output of sample must be a float or array
    assert isinstance(sample(X), (numpy.int32, numpy.int64))
    assert isinstance(sample(Y), numpy.float64)
    assert isinstance(sample(X, size=2), numpy.ndarray)

    with warns_deprecated_sympy():
        sample(X, numsamples=2)

