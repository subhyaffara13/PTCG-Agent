
def test_gruntz_eval_special_slow():
    _sskip()
    assert gruntz(gamma(x + 1)/sqrt(2*pi)
                  - exp(-x)*(x**(x + S.Half) + x**(x - S.Half)/12), x, oo) is oo
    assert gruntz(exp(exp(exp(digamma(digamma(digamma(x))))))/x, x, oo) == 0

