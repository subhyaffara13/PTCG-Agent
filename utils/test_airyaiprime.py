
def test_airyaiprime():
    z = Symbol('z', real=False)
    t = Symbol('t', negative=True)
    p = Symbol('p', positive=True)

    assert isinstance(airyaiprime(z), airyaiprime)

    assert airyaiprime(0) == -3**Rational(2, 3)/(3*gamma(Rational(1, 3)))
    assert airyaiprime(oo) == 0

    assert diff(airyaiprime(z), z) == z*airyai(z)

    assert series(airyaiprime(z), z, 0, 3) == (
        -3**Rational(2, 3)/(3*gamma(Rational(1, 3))) + 3**Rational(1, 3)*z**2/(6*gamma(Rational(2, 3))) + O(z**3))

    assert airyaiprime(z).rewrite(hyper) == (
        3**Rational(1, 3)*z**2*hyper((), (Rational(5, 3),), z**3/9)/(6*gamma(Rational(2, 3))) -
        3**Rational(2, 3)*hyper((), (Rational(1, 3),), z**3/9)/(3*gamma(Rational(1, 3))))

    assert isinstance(airyaiprime(z).rewrite(besselj), airyaiprime)
    assert airyai(t).rewrite(besselj) == (
        sqrt(-t)*(besselj(Rational(-1, 3), 2*(-t)**Rational(3, 2)/3) +
                  besselj(Rational(1, 3), 2*(-t)**Rational(3, 2)/3))/3)
    assert airyaiprime(z).rewrite(besseli) == (
        z**2*besseli(Rational(2, 3), 2*z**Rational(3, 2)/3)/(3*(z**Rational(3, 2))**Rational(2, 3)) -
        (z**Rational(3, 2))**Rational(2, 3)*besseli(Rational(-1, 3), 2*z**Rational(3, 2)/3)/3)
    assert airyaiprime(p).rewrite(besseli) == (
        p*(-besseli(Rational(-2, 3), 2*p**Rational(3, 2)/3) + besseli(Rational(2, 3), 2*p**Rational(3, 2)/3))/3)

    assert expand_func(airyaiprime(2*(3*z**5)**Rational(1, 3))) == (
        sqrt(3)*(z**Rational(5, 3)/(z**5)**Rational(1, 3) - 1)*airybiprime(2*3**Rational(1, 3)*z**Rational(5, 3))/6 +
        (z**Rational(5, 3)/(z**5)**Rational(1, 3) + 1)*airyaiprime(2*3**Rational(1, 3)*z**Rational(5, 3))/2)

