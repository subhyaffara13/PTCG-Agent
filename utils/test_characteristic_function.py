
def test_characteristic_function():
    X = Uniform('x', 0, 1)

    cf = characteristic_function(X)
    assert cf(1) == -I*(-1 + exp(I))

    Y = Normal('y', 1, 1)
    cf = characteristic_function(Y)
    assert cf(0) == 1
    assert cf(1) == exp(I - S.Half)

    Z = Exponential('z', 5)
    cf = characteristic_function(Z)
    assert cf(0) == 1
    assert cf(1).expand() == Rational(25, 26) + I*5/26

    X = GaussianInverse('x', 1, 1)
    cf = characteristic_function(X)
    assert cf(0) == 1
    assert cf(1) == exp(1 - sqrt(1 - 2*I))

    X = ExGaussian('x', 0, 1, 1)
    cf = characteristic_function(X)
    assert cf(0) == 1
    assert cf(1) == (1 + I)*exp(Rational(-1, 2))/2

    L = Levy('x', 0, 1)
    cf = characteristic_function(L)
    assert cf(0) == 1
    assert cf(1) == exp(-sqrt(2)*sqrt(-I))


def test_characteristic_function():
    #  Imports I from sympy
    from sympy.core.numbers import I
    X = Normal('X',0,1)
    Y = DiscreteUniform('Y', [1,2,7])
    Z = Poisson('Z', 2)
    t = symbols('_t')
    P = Lambda(t, exp(-t**2/2))
    Q = Lambda(t, exp(7*t*I)/3 + exp(2*t*I)/3 + exp(t*I)/3)
    R = Lambda(t, exp(2 * exp(t*I) - 2))


    assert characteristic_function(X).dummy_eq(P)
    assert characteristic_function(Y).dummy_eq(Q)
    assert characteristic_function(Z).dummy_eq(R)

