import re

def test_erfc():
    assert erfc(nan) is nan

    assert erfc(oo) is S.Zero
    assert erfc(-oo) == 2

    assert erfc(0) == 1

    assert erfc(I*oo) == -oo*I
    assert erfc(-I*oo) == oo*I

    assert erfc(-x) == S(2) - erfc(x)
    assert erfc(erfcinv(x)) == x

    alpha = symbols('alpha', extended_real=True)
    assert erfc(alpha).is_real is True
    alpha = symbols('alpha', extended_real=False)
    assert erfc(alpha).is_real is None
    assert erfc(I).is_real is False
    assert erfc(0, evaluate=False).is_real
    assert erfc(0, evaluate=False).is_zero is False

    assert erfc(erfinv(x)) == 1 - x

    assert conjugate(erfc(z)) == erfc(conjugate(z))

    assert erfc(x).as_leading_term(x) is S.One
    assert erfc(1/x).as_leading_term(x) == S.Zero

    assert erfc(z).rewrite('erf') == 1 - erf(z)
    assert erfc(z).rewrite('erfi') == 1 + I*erfi(I*z)
    assert erfc(z).rewrite('fresnels') == 1 - (1 + I)*(fresnelc(z*(1 - I)/sqrt(pi)) -
        I*fresnels(z*(1 - I)/sqrt(pi)))
    assert erfc(z).rewrite('fresnelc') == 1 - (1 + I)*(fresnelc(z*(1 - I)/sqrt(pi)) -
        I*fresnels(z*(1 - I)/sqrt(pi)))
    assert erfc(z).rewrite('hyper') == 1 - 2*z*hyper([S.Half], [3*S.Half], -z**2)/sqrt(pi)
    assert erfc(z).rewrite('meijerg') == 1 - z*meijerg([S.Half], [], [0], [Rational(-1, 2)], z**2)/sqrt(pi)
    assert erfc(z).rewrite('uppergamma') == 1 - sqrt(z**2)*(1 - erfc(sqrt(z**2)))/z
    assert erfc(z).rewrite('expint') == S.One - sqrt(z**2)/z + z*expint(S.Half, z**2)/sqrt(S.Pi)
    assert erfc(z).rewrite('tractable') == _erfs(z)*exp(-z**2)
    assert expand_func(erf(x) + erfc(x)) is S.One

    assert erfc(x).as_real_imag() == \
        (erfc(re(x) - I*im(x))/2 + erfc(re(x) + I*im(x))/2,
         -I*(-erfc(re(x) - I*im(x)) + erfc(re(x) + I*im(x)))/2)

    assert erfc(x).as_real_imag(deep=False) == \
        (erfc(re(x) - I*im(x))/2 + erfc(re(x) + I*im(x))/2,
         -I*(-erfc(re(x) - I*im(x)) + erfc(re(x) + I*im(x)))/2)

    assert erfc(w).as_real_imag() == (erfc(w), 0)
    assert erfc(w).as_real_imag(deep=False) == (erfc(w), 0)
    raises(ArgumentIndexError, lambda: erfc(x).fdiff(2))

    assert erfc(x).inverse() == erfcinv

