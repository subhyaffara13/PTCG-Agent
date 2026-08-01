
def test_aseries_trig():
    assert cancel(gruntz(1/log(atan(x)), x, oo)
           - 1/(log(pi) + log(S.Half))) == 0
    assert gruntz(1/acot(x), x, -oo) is -oo

