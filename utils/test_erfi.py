import re

def test_erfi():
    assert erfi(nan) is nan

    assert erfi(oo) is S.Infinity
    assert erfi(-oo) is S.NegativeInfinity

    assert erfi(0) is S.Zero

    assert erfi(I*oo) == I
    assert erfi(-I*oo) == -I

    assert erfi(-x) == -erfi(x)

    assert erfi(I*erfinv(x)) == I*x
    assert erfi(I*erfcinv(x)) == I*(1 - x)
    assert erfi(I*erf2inv(0, x)) == I*x
    assert erfi(I*erf2inv(0, x, evaluate=False)) == I*x # To cover code in erfi

    assert erfi(I).is_real is False
    assert erfi(0, evaluate=False).is_real
    assert erfi(0, evaluate=False).is_zero

    assert conjugate(erfi(z)) == erfi(conjugate(z))

    assert erfi(x).as_leading_term(x) == 2*x/sqrt(pi)
    assert erfi(x*y).as_leading_term(y) == 2*x*y/sqrt(pi)
    assert (erfi(x*y)/erfi(y)).as_leading_term(y) == x
    assert erfi(1/x).as_leading_term(x) == erfi(1/x)

    assert erfi(z).rewrite('erf') == -I*erf(I*z)
    assert erfi(z).rewrite('erfc') == I*erfc(I*z) - I
    assert erfi(z).rewrite('fresnels') == (1 - I)*(fresnelc(z*(1 + I)/sqrt(pi)) -
        I*fresnels(z*(1 + I)/sqrt(pi)))
    assert erfi(z).rewrite('fresnelc') == (1 - I)*(fresnelc(z*(1 + I)/sqrt(pi)) -
        I*fresnels(z*(1 + I)/sqrt(pi)))
    assert erfi(z).rewrite('hyper') == 2*z*hyper([S.Half], [3*S.Half], z**2)/sqrt(pi)
    assert erfi(z).rewrite('meijerg') == z*meijerg([S.Half], [], [0], [Rational(-1, 2)], -z**2)/sqrt(pi)
    assert erfi(z).rewrite('uppergamma') == (sqrt(-z**2)/z*(uppergamma(S.Half,
        -z**2)/sqrt(S.Pi) - S.One))
    assert erfi(z).rewrite('expint') == sqrt(-z**2)/z - z*expint(S.Half, -z**2)/sqrt(S.Pi)
    assert erfi(z).rewrite('tractable') == -I*(-_erfs(I*z)*exp(z**2) + 1)
    assert expand_func(erfi(I*z)) == I*erf(z)

    assert erfi(x).as_real_imag() == \
        (erfi(re(x) - I*im(x))/2 + erfi(re(x) + I*im(x))/2,
         -I*(-erfi(re(x) - I*im(x)) + erfi(re(x) + I*im(x)))/2)
    assert erfi(x).as_real_imag(deep=False) == \
        (erfi(re(x) - I*im(x))/2 + erfi(re(x) + I*im(x))/2,
         -I*(-erfi(re(x) - I*im(x)) + erfi(re(x) + I*im(x)))/2)

    assert erfi(w).as_real_imag() == (erfi(w), 0)
    assert erfi(w).as_real_imag(deep=False) == (erfi(w), 0)

    raises(ArgumentIndexError, lambda: erfi(x).fdiff(2))

