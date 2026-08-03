import re

def test_fresnel():
    from sympy.functions.special.error_functions import (fresnelc, fresnels)

    assert expand_func(integrate(sin(pi*x**2/2), x)) == fresnels(x)
    assert expand_func(integrate(cos(pi*x**2/2), x)) == fresnelc(x)


def test_fresnel():
    assert fresnels(0) is S.Zero
    assert fresnels(oo) is S.Half
    assert fresnels(-oo) == Rational(-1, 2)
    assert fresnels(I*oo) == -I*S.Half

    assert unchanged(fresnels, z)
    assert fresnels(-z) == -fresnels(z)
    assert fresnels(I*z) == -I*fresnels(z)
    assert fresnels(-I*z) == I*fresnels(z)

    assert conjugate(fresnels(z)) == fresnels(conjugate(z))

    assert fresnels(z).diff(z) == sin(pi*z**2/2)

    assert fresnels(z).rewrite(erf) == (S.One + I)/4 * (
        erf((S.One + I)/2*sqrt(pi)*z) - I*erf((S.One - I)/2*sqrt(pi)*z))

    assert fresnels(z).rewrite(hyper) == \
        pi*z**3/6 * hyper([Rational(3, 4)], [Rational(3, 2), Rational(7, 4)], -pi**2*z**4/16)

    assert fresnels(z).series(z, n=15) == \
        pi*z**3/6 - pi**3*z**7/336 + pi**5*z**11/42240 + O(z**15)

    assert fresnels(w).is_extended_real is True
    assert fresnels(w).is_finite is True

    assert fresnels(z).is_extended_real is None
    assert fresnels(z).is_finite is None

    assert fresnels(z).as_real_imag() == (fresnels(re(z) - I*im(z))/2 +
                    fresnels(re(z) + I*im(z))/2,
                    -I*(-fresnels(re(z) - I*im(z)) + fresnels(re(z) + I*im(z)))/2)

    assert fresnels(z).as_real_imag(deep=False) == (fresnels(re(z) - I*im(z))/2 +
                    fresnels(re(z) + I*im(z))/2,
                    -I*(-fresnels(re(z) - I*im(z)) + fresnels(re(z) + I*im(z)))/2)

    assert fresnels(w).as_real_imag() == (fresnels(w), 0)
    assert fresnels(w).as_real_imag(deep=True) == (fresnels(w), 0)

    assert fresnels(2 + 3*I).as_real_imag() == (
            fresnels(2 + 3*I)/2 + fresnels(2 - 3*I)/2,
            -I*(fresnels(2 + 3*I) - fresnels(2 - 3*I))/2
            )

    assert expand_func(integrate(fresnels(z), z)) == \
        z*fresnels(z) + cos(pi*z**2/2)/pi

    assert fresnels(z).rewrite(meijerg) == sqrt(2)*pi*z**Rational(9, 4) * \
        meijerg(((), (1,)), ((Rational(3, 4),),
        (Rational(1, 4), 0)), -pi**2*z**4/16)/(2*(-z)**Rational(3, 4)*(z**2)**Rational(3, 4))

    assert fresnelc(0) is S.Zero
    assert fresnelc(oo) == S.Half
    assert fresnelc(-oo) == Rational(-1, 2)
    assert fresnelc(I*oo) == I*S.Half

    assert unchanged(fresnelc, z)
    assert fresnelc(-z) == -fresnelc(z)
    assert fresnelc(I*z) == I*fresnelc(z)
    assert fresnelc(-I*z) == -I*fresnelc(z)

    assert conjugate(fresnelc(z)) == fresnelc(conjugate(z))

    assert fresnelc(z).diff(z) == cos(pi*z**2/2)

    assert fresnelc(z).rewrite(erf) == (S.One - I)/4 * (
        erf((S.One + I)/2*sqrt(pi)*z) + I*erf((S.One - I)/2*sqrt(pi)*z))

    assert fresnelc(z).rewrite(hyper) == \
        z * hyper([Rational(1, 4)], [S.Half, Rational(5, 4)], -pi**2*z**4/16)

    assert fresnelc(w).is_extended_real is True

    assert fresnelc(z).as_real_imag() == \
        (fresnelc(re(z) - I*im(z))/2 + fresnelc(re(z) + I*im(z))/2,
         -I*(-fresnelc(re(z) - I*im(z)) + fresnelc(re(z) + I*im(z)))/2)

    assert fresnelc(z).as_real_imag(deep=False) == \
        (fresnelc(re(z) - I*im(z))/2 + fresnelc(re(z) + I*im(z))/2,
         -I*(-fresnelc(re(z) - I*im(z)) + fresnelc(re(z) + I*im(z)))/2)

    assert fresnelc(2 + 3*I).as_real_imag() == (
        fresnelc(2 - 3*I)/2 + fresnelc(2 + 3*I)/2,
         -I*(fresnelc(2 + 3*I) - fresnelc(2 - 3*I))/2
    )

    assert expand_func(integrate(fresnelc(z), z)) == \
        z*fresnelc(z) - sin(pi*z**2/2)/pi

    assert fresnelc(z).rewrite(meijerg) == sqrt(2)*pi*z**Rational(3, 4) * \
        meijerg(((), (1,)), ((Rational(1, 4),),
        (Rational(3, 4), 0)), -pi**2*z**4/16)/(2*(-z)**Rational(1, 4)*(z**2)**Rational(1, 4))

    from sympy.core.random import verify_numerically

    verify_numerically(re(fresnels(z)), fresnels(z).as_real_imag()[0], z)
    verify_numerically(im(fresnels(z)), fresnels(z).as_real_imag()[1], z)
    verify_numerically(fresnels(z), fresnels(z).rewrite(hyper), z)
    verify_numerically(fresnels(z), fresnels(z).rewrite(meijerg), z)

    verify_numerically(re(fresnelc(z)), fresnelc(z).as_real_imag()[0], z)
    verify_numerically(im(fresnelc(z)), fresnelc(z).as_real_imag()[1], z)
    verify_numerically(fresnelc(z), fresnelc(z).rewrite(hyper), z)
    verify_numerically(fresnelc(z), fresnelc(z).rewrite(meijerg), z)

    raises(ArgumentIndexError, lambda: fresnels(z).fdiff(2))
    raises(ArgumentIndexError, lambda: fresnelc(z).fdiff(2))

    assert fresnels(x).taylor_term(-1, x) is S.Zero
    assert fresnelc(x).taylor_term(-1, x) is S.Zero
    assert fresnelc(x).taylor_term(1, x) == -pi**2*x**5/40

