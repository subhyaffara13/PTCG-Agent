import re

def test_erf():
    assert erf(nan) is nan

    assert erf(oo) == 1
    assert erf(-oo) == -1

    assert erf(0) is S.Zero

    assert erf(I*oo) == oo*I
    assert erf(-I*oo) == -oo*I

    assert erf(-2) == -erf(2)
    assert erf(-x*y) == -erf(x*y)
    assert erf(-x - y) == -erf(x + y)

    assert erf(erfinv(x)) == x
    assert erf(erfcinv(x)) == 1 - x
    assert erf(erf2inv(0, x)) == x
    assert erf(erf2inv(0, x, evaluate=False)) == x # To cover code in erf
    assert erf(erf2inv(0, erf(erfcinv(1 - erf(erfinv(x)))))) == x

    alpha = symbols('alpha', extended_real=True)
    assert erf(alpha).is_real is True
    assert erf(alpha).is_finite is True
    alpha = symbols('alpha', extended_real=False)
    assert erf(alpha).is_real is None
    assert erf(alpha).is_finite is None
    assert erf(alpha).is_zero is None
    assert erf(alpha).is_positive is None
    assert erf(alpha).is_negative is None
    alpha = symbols('alpha', extended_positive=True)
    assert erf(alpha).is_positive is True
    alpha = symbols('alpha', extended_negative=True)
    assert erf(alpha).is_negative is True
    assert erf(I).is_real is False
    assert erf(0, evaluate=False).is_real
    assert erf(0, evaluate=False).is_zero

    assert conjugate(erf(z)) == erf(conjugate(z))

    assert erf(x).as_leading_term(x) == 2*x/sqrt(pi)
    assert erf(x*y).as_leading_term(y) == 2*x*y/sqrt(pi)
    assert (erf(x*y)/erf(y)).as_leading_term(y) == x
    assert erf(1/x).as_leading_term(x) == S.One

    assert erf(z).rewrite('uppergamma') == sqrt(z**2)*(1 - erfc(sqrt(z**2)))/z
    assert erf(z).rewrite('erfc') == S.One - erfc(z)
    assert erf(z).rewrite('erfi') == -I*erfi(I*z)
    assert erf(z).rewrite('fresnels') == (1 + I)*(fresnelc(z*(1 - I)/sqrt(pi)) -
        I*fresnels(z*(1 - I)/sqrt(pi)))
    assert erf(z).rewrite('fresnelc') == (1 + I)*(fresnelc(z*(1 - I)/sqrt(pi)) -
        I*fresnels(z*(1 - I)/sqrt(pi)))
    assert erf(z).rewrite('hyper') == 2*z*hyper([S.Half], [3*S.Half], -z**2)/sqrt(pi)
    assert erf(z).rewrite('meijerg') == z*meijerg([S.Half], [], [0], [Rational(-1, 2)], z**2)/sqrt(pi)
    assert erf(z).rewrite('expint') == sqrt(z**2)/z - z*expint(S.Half, z**2)/sqrt(S.Pi)

    assert limit(exp(x)*exp(x**2)*(erf(x + 1/exp(x)) - erf(x)), x, oo) == \
        2/sqrt(pi)
    assert limit((1 - erf(z))*exp(z**2)*z, z, oo) == 1/sqrt(pi)
    assert limit((1 - erf(x))*exp(x**2)*sqrt(pi)*x, x, oo) == 1
    assert limit(((1 - erf(x))*exp(x**2)*sqrt(pi)*x - 1)*2*x**2, x, oo) == -1
    assert limit(erf(x)/x, x, 0) == 2/sqrt(pi)
    assert limit(x**(-4) - sqrt(pi)*erf(x**2) / (2*x**6), x, 0) == S(1)/3

    assert erf(x).as_real_imag() == \
        (erf(re(x) - I*im(x))/2 + erf(re(x) + I*im(x))/2,
         -I*(-erf(re(x) - I*im(x)) + erf(re(x) + I*im(x)))/2)

    assert erf(x).as_real_imag(deep=False) == \
        (erf(re(x) - I*im(x))/2 + erf(re(x) + I*im(x))/2,
         -I*(-erf(re(x) - I*im(x)) + erf(re(x) + I*im(x)))/2)

    assert erf(w).as_real_imag() == (erf(w), 0)
    assert erf(w).as_real_imag(deep=False) == (erf(w), 0)
    # issue 13575
    assert erf(I).as_real_imag() == (0, -I*erf(I))

    raises(ArgumentIndexError, lambda: erf(x).fdiff(2))

    assert erf(x).inverse() == erfinv


def test_erf():
    mp.dps = 15
    assert erf(0) == 0
    assert erf(1).ae(0.84270079294971486934)
    assert erf(3+4j).ae(-120.186991395079444098 - 27.750337293623902498j)
    assert erf(-4-3j).ae(-0.99991066178539168236 + 0.00004972026054496604j)
    assert erf(pi).ae(0.99999112385363235839)
    assert erf(1j).ae(1.6504257587975428760j)
    assert erf(-1j).ae(-1.6504257587975428760j)
    assert isinstance(erf(1), mpf)
    assert isinstance(erf(-1), mpf)
    assert isinstance(erf(0), mpf)
    assert isinstance(erf(0j), mpc)
    assert erf(inf) == 1
    assert erf(-inf) == -1
    assert erfi(0) == 0
    assert erfi(1/pi).ae(0.371682698493894314)
    assert erfi(inf) == inf
    assert erfi(-inf) == -inf
    assert erf(1+0j) == erf(1)
    assert erfc(1+0j) == erfc(1)
    assert erf(0.2+0.5j).ae(1 - erfc(0.2+0.5j))
    assert erfc(0) == 1
    assert erfc(1).ae(1-erf(1))
    assert erfc(-1).ae(1-erf(-1))
    assert erfc(1/pi).ae(1-erf(1/pi))
    assert erfc(-10) == 2
    assert erfc(-1000000) == 2
    assert erfc(-inf) == 2
    assert erfc(inf) == 0
    assert isnan(erfc(nan))
    assert (erfc(10**4)*mpf(10)**43429453).ae('3.63998738656420')
    assert erf(8+9j).ae(-1072004.2525062051158 + 364149.91954310255423j)
    assert erfc(8+9j).ae(1072005.2525062051158 - 364149.91954310255423j)
    assert erfc(-8-9j).ae(-1072003.2525062051158 + 364149.91954310255423j)
    mp.dps = 50
    # This one does not use the asymptotic series
    assert (erfc(10)*10**45).ae('2.0884875837625447570007862949577886115608181193212')
    # This one does
    assert (erfc(50)*10**1088).ae('2.0709207788416560484484478751657887929322509209954')
    mp.dps = 15
    assert str(erfc(10**50)) == '3.66744826532555e-4342944819032518276511289189166050822943970058036665661144537831658646492088707747292249493384317534'
    assert erfinv(0) == 0
    assert erfinv(0.5).ae(0.47693627620446987338)
    assert erfinv(-0.5).ae(-0.47693627620446987338)
    assert erfinv(1) == inf
    assert erfinv(-1) == -inf
    assert erf(erfinv(0.95)).ae(0.95)
    assert erf(erfinv(0.999999999995)).ae(0.999999999995)
    assert erf(erfinv(-0.999999999995)).ae(-0.999999999995)
    mp.dps = 50
    assert erf(erfinv('0.99999999999999999999999999999995')).ae('0.99999999999999999999999999999995')
    assert erf(erfinv('0.999999999999999999999999999999995')).ae('0.999999999999999999999999999999995')
    assert erf(erfinv('-0.999999999999999999999999999999995')).ae('-0.999999999999999999999999999999995')
    mp.dps = 15
    # Complex asymptotic expansions
    v = erfc(50j)
    assert v.real == 1
    assert v.imag.ae('-6.1481820666053078736e+1083')
    assert erfc(-100+5j).ae(2)
    assert (erfc(100+5j)*10**4335).ae(2.3973567853824133572 - 3.9339259530609420597j)
    assert erfc(100+100j).ae(0.00065234366376857698698 - 0.0039357263629214118437j)

