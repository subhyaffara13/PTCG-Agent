
def test_gruntz_evaluation_slow():
    _sskip()
    # 8.4
    assert gruntz(exp(exp(exp(x)/(1 - 1/x)))
                  - exp(exp(exp(x)/(1 - 1/x - log(x)**(-log(x))))), x, oo) is -oo
    # 8.18
    assert gruntz((exp(exp(-x/(1 + exp(-x))))*exp(-x/(1 + exp(-x/(1 + exp(-x)))))
                   *exp(exp(-x + exp(-x/(1 + exp(-x))))))
                  / (exp(-x/(1 + exp(-x))))**2 - exp(x) + x, x, oo) == 2

