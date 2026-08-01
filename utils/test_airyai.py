
def test_airyai():
    z = Symbol('z', real=False)
    t = Symbol('t', negative=True)
    p = Symbol('p', positive=True)

    assert isinstance(airyai(z), airyai)

    assert airyai(0) == 3**Rational(1, 3)/(3*gamma(Rational(2, 3)))
    assert airyai(oo) == 0
    assert airyai(-oo) == 0

    assert diff(airyai(z), z) == airyaiprime(z)

    assert series(airyai(z), z, 0, 3) == (
        3**Rational(5, 6)*gamma(Rational(1, 3))/(6*pi) - 3**Rational(1, 6)*z*gamma(Rational(2, 3))/(2*pi) + O(z**3))

    assert airyai(z).rewrite(hyper) == (
        -3**Rational(2, 3)*z*hyper((), (Rational(4, 3),), z**3/9)/(3*gamma(Rational(1, 3))) +
         3**Rational(1, 3)*hyper((), (Rational(2, 3),), z**3/9)/(3*gamma(Rational(2, 3))))

    assert isinstance(airyai(z).rewrite(besselj), airyai)
    assert airyai(t).rewrite(besselj) == (
        sqrt(-t)*(besselj(Rational(-1, 3), 2*(-t)**Rational(3, 2)/3) +
                  besselj(Rational(1, 3), 2*(-t)**Rational(3, 2)/3))/3)
    assert airyai(z).rewrite(besseli) == (
        -z*besseli(Rational(1, 3), 2*z**Rational(3, 2)/3)/(3*(z**Rational(3, 2))**Rational(1, 3)) +
         (z**Rational(3, 2))**Rational(1, 3)*besseli(Rational(-1, 3), 2*z**Rational(3, 2)/3)/3)
    assert airyai(p).rewrite(besseli) == (
        sqrt(p)*(besseli(Rational(-1, 3), 2*p**Rational(3, 2)/3) -
                 besseli(Rational(1, 3), 2*p**Rational(3, 2)/3))/3)

    assert expand_func(airyai(2*(3*z**5)**Rational(1, 3))) == (
        -sqrt(3)*(-1 + (z**5)**Rational(1, 3)/z**Rational(5, 3))*airybi(2*3**Rational(1, 3)*z**Rational(5, 3))/6 +
         (1 + (z**5)**Rational(1, 3)/z**Rational(5, 3))*airyai(2*3**Rational(1, 3)*z**Rational(5, 3))/2)

