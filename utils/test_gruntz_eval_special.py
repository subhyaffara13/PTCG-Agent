
def test_gruntz_eval_special():
    # Gruntz, p. 126
    assert gruntz(exp(x)*(sin(1/x + exp(-x)) - sin(1/x + exp(-x**2))), x, oo) == 1
    assert gruntz((erf(x - exp(-exp(x))) - erf(x)) * exp(exp(x)) * exp(x**2),
                  x, oo) == -2/sqrt(pi)
    assert gruntz(exp(exp(x)) * (exp(sin(1/x + exp(-exp(x)))) - exp(sin(1/x))),
                  x, oo) == 1
    assert gruntz(exp(x)*(gamma(x + exp(-x)) - gamma(x)), x, oo) is oo
    assert gruntz(exp(exp(digamma(digamma(x))))/x, x, oo) == exp(Rational(-1, 2))
    assert gruntz(exp(exp(digamma(log(x))))/x, x, oo) == exp(Rational(-1, 2))
    assert gruntz(digamma(digamma(digamma(x))), x, oo) is oo
    assert gruntz(loggamma(loggamma(x)), x, oo) is oo
    assert gruntz(((gamma(x + 1/gamma(x)) - gamma(x))/log(x) - cos(1/x))
                  * x*log(x), x, oo) == Rational(-1, 2)
    assert gruntz(x * (gamma(x - 1/gamma(x)) - gamma(x) + log(x)), x, oo) \
        == S.Half
    assert gruntz((gamma(x + 1/gamma(x)) - gamma(x)) / log(x), x, oo) == 1

