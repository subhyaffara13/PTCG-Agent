
def test_exp_log_series():
    assert gruntz(x/log(log(x*exp(x))), x, oo) is oo

