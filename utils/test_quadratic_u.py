
def test_quadratic_u():
    a = Symbol("a", real=True)
    b = Symbol("b", real=True)

    X = QuadraticU("x", a, b)
    Y = QuadraticU("x", 1, 2)

    assert pspace(X).domain.set == Interval(a, b)
    # Tests _moment_generating_function
    assert moment_generating_function(Y)(1)  == -15*exp(2) + 27*exp(1)
    assert moment_generating_function(Y)(2) == -9*exp(4)/2 + 21*exp(2)/2

    assert characteristic_function(Y)(1) == 3*I*(-1 + 4*I)*exp(I*exp(2*I))
    assert density(X)(x) == (Piecewise((12*(x - a/2 - b/2)**2/(-a + b)**3,
                          And(x <= b, a <= x)), (0, True)))

