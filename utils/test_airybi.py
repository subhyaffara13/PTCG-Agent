
def test_airybi():
    z = Symbol('z', real=False)
    t = Symbol('t', negative=True)
    p = Symbol('p', positive=True)

    assert isinstance(airybi(z), airybi)

    assert airybi(0) == 3**Rational(5, 6)/(3*gamma(Rational(2, 3)))
    assert airybi(oo) is oo
    assert airybi(-oo) == 0

    assert diff(airybi(z), z) == airybiprime(z)

    assert series(airybi(z), z, 0, 3) == (
        3**Rational(1, 3)*gamma(Rational(1, 3))/(2*pi) + 3**Rational(2, 3)*z*gamma(Rational(2, 3))/(2*pi) + O(z**3))

    assert airybi(z).rewrite(hyper) == (
        3**Rational(1, 6)*z*hyper((), (Rational(4, 3),), z**3/9)/gamma(Rational(1, 3)) +
        3**Rational(5, 6)*hyper((), (Rational(2, 3),), z**3/9)/(3*gamma(Rational(2, 3))))

    assert isinstance(airybi(z).rewrite(besselj), airybi)
    assert airyai(t).rewrite(besselj) == (
        sqrt(-t)*(besselj(Rational(-1, 3), 2*(-t)**Rational(3, 2)/3) +
                  besselj(Rational(1, 3), 2*(-t)**Rational(3, 2)/3))/3)
    assert airybi(z).rewrite(besseli) == (
        sqrt(3)*(z*besseli(Rational(1, 3), 2*z**Rational(3, 2)/3)/(z**Rational(3, 2))**Rational(1, 3) +
                 (z**Rational(3, 2))**Rational(1, 3)*besseli(Rational(-1, 3), 2*z**Rational(3, 2)/3))/3)
    assert airybi(p).rewrite(besseli) == (
        sqrt(3)*sqrt(p)*(besseli(Rational(-1, 3), 2*p**Rational(3, 2)/3) +
                         besseli(Rational(1, 3), 2*p**Rational(3, 2)/3))/3)

    assert expand_func(airybi(2*(3*z**5)**Rational(1, 3))) == (
        sqrt(3)*(1 - (z**5)**Rational(1, 3)/z**Rational(5, 3))*airyai(2*3**Rational(1, 3)*z**Rational(5, 3))/2 +
        (1 + (z**5)**Rational(1, 3)/z**Rational(5, 3))*airybi(2*3**Rational(1, 3)*z**Rational(5, 3))/2)

