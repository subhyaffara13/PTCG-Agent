
def test_Hermite():
    a1 = Symbol("a1", positive=True)
    a2 = Symbol("a2", negative=True)
    raises(ValueError, lambda: Hermite("H", a1, a2))

    a1 = Symbol("a1", negative=True)
    a2 = Symbol("a2", positive=True)
    raises(ValueError, lambda: Hermite("H", a1, a2))

    a1 = Symbol("a1", positive=True)
    x = Symbol("x")
    H = Hermite("H", a1, a2)
    assert moment_generating_function(H)(x) == exp(a1*(exp(x) - 1)
                                            + a2*(exp(2*x) - 1))
    assert characteristic_function(H)(x) == exp(a1*(exp(I*x) - 1)
                                            + a2*(exp(2*I*x) - 1))
    assert E(H) == a1 + 2*a2

    H = Hermite("H", a1=5, a2=4)
    assert density(H)(2) == 33*exp(-9)/2
    assert E(H) == 13
    assert variance(H) == 21
    assert kurtosis(H) == Rational(464,147)
    assert skewness(H) == 37*sqrt(21)/441

