
def test_besselsimp():
    from sympy.functions.special.bessel import (besseli, besselj, bessely)
    from sympy.integrals.transforms import cosine_transform
    assert besselsimp(exp(-I*pi*y/2)*besseli(y, z*exp_polar(I*pi/2))) == \
        besselj(y, z)
    assert besselsimp(exp(-I*pi*a/2)*besseli(a, 2*sqrt(x)*exp_polar(I*pi/2))) == \
        besselj(a, 2*sqrt(x))
    assert besselsimp(sqrt(2)*sqrt(pi)*x**Rational(1, 4)*exp(I*pi/4)*exp(-I*pi*a/2) *
                      besseli(Rational(-1, 2), sqrt(x)*exp_polar(I*pi/2)) *
                      besseli(a, sqrt(x)*exp_polar(I*pi/2))/2) == \
        besselj(a, sqrt(x)) * cos(sqrt(x))
    assert besselsimp(besseli(Rational(-1, 2), z)) == \
        sqrt(2)*cosh(z)/(sqrt(pi)*sqrt(z))
    assert besselsimp(besseli(a, z*exp_polar(-I*pi/2))) == \
        exp(-I*pi*a/2)*besselj(a, z)
    assert cosine_transform(1/t*sin(a/t), t, y) == \
        sqrt(2)*sqrt(pi)*besselj(0, 2*sqrt(a)*sqrt(y))/2

    assert besselsimp(x**2*(a*(-2*besselj(5*I, x) + besselj(-2 + 5*I, x) +
    besselj(2 + 5*I, x)) + b*(-2*bessely(5*I, x) + bessely(-2 + 5*I, x) +
    bessely(2 + 5*I, x)))/4 + x*(a*(besselj(-1 + 5*I, x)/2 - besselj(1 + 5*I, x)/2)
    + b*(bessely(-1 + 5*I, x)/2 - bessely(1 + 5*I, x)/2)) + (x**2 + 25)*(a*besselj(5*I, x)
    + b*bessely(5*I, x))) == 0

    assert besselsimp(81*x**2*(a*(besselj(Rational(-5, 3), 9*x) - 2*besselj(Rational(1, 3), 9*x) + besselj(Rational(7, 3), 9*x))
    + b*(bessely(Rational(-5, 3), 9*x) - 2*bessely(Rational(1, 3), 9*x) + bessely(Rational(7, 3), 9*x)))/4 + x*(a*(9*besselj(Rational(-2, 3), 9*x)/2
    - 9*besselj(Rational(4, 3), 9*x)/2) + b*(9*bessely(Rational(-2, 3), 9*x)/2 - 9*bessely(Rational(4, 3), 9*x)/2)) +
    (81*x**2 - Rational(1, 9))*(a*besselj(Rational(1, 3), 9*x) + b*bessely(Rational(1, 3), 9*x))) == 0

    assert besselsimp(besselj(a-1,x) + besselj(a+1, x) - 2*a*besselj(a, x)/x) == 0

    assert besselsimp(besselj(a-1,x) + besselj(a+1, x) + besselj(a, x)) == (2*a + x)*besselj(a, x)/x

    assert besselsimp(x**2* besselj(a,x) + x**3*besselj(a+1, x) + besselj(a+2, x)) == \
    2*a*x*besselj(a + 1, x) + x**3*besselj(a + 1, x) - x**2*besselj(a + 2, x) + 2*x*besselj(a + 1, x) + besselj(a + 2, x)

