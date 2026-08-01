
def test_gruntz_eval_special_fail():
    # TODO zeta function series
    assert gruntz(
        exp((log(2) + 1)*x) * (zeta(x + exp(-x)) - zeta(x)), x, oo) == -log(2)

