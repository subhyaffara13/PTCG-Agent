
def test_gruntz_Ei():
    assert gruntz((Ei(x - exp(-exp(x))) - Ei(x)) *exp(-x)*exp(exp(x))*x, x, oo) == -1

