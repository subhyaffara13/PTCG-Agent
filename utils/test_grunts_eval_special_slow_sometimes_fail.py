
def test_grunts_eval_special_slow_sometimes_fail():
    _sskip()
    # XXX This sometimes fails!!!
    assert gruntz(exp(gamma(x - exp(-x))*exp(1/x)) - exp(gamma(x)), x, oo) is oo

