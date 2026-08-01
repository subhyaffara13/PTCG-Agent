
def test_chi():
    from sympy.core.numbers import I
    k = Symbol("k", integer=True)

    X = Chi('x', k)
    assert density(X)(x) == 2**(-k/2 + 1)*x**(k - 1)*exp(-x**2/2)/gamma(k/2)

    # Tests the characteristic function
    assert characteristic_function(X)(x) == sqrt(2)*I*x*gamma(k/2 + S(1)/2)*hyper((k/2 + S(1)/2,),
                                            (S(3)/2,), -x**2/2)/gamma(k/2) + hyper((k/2,), (S(1)/2,), -x**2/2)

    # Tests the moment generating function
    assert moment_generating_function(X)(x) == sqrt(2)*x*gamma(k/2 + S(1)/2)*hyper((k/2 + S(1)/2,),
                                                (S(3)/2,), x**2/2)/gamma(k/2) + hyper((k/2,), (S(1)/2,), x**2/2)

    k = Symbol("k", integer=True, positive=False)
    raises(ValueError, lambda: Chi('x', k))

    k = Symbol("k", integer=False, positive=True)
    raises(ValueError, lambda: Chi('x', k))

