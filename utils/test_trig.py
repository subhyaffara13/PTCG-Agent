
def test_trig():
    f = lambdify([x], [cos(x), sin(x)], 'math')
    d = f(pi)
    prec = 1e-11
    assert -prec < d[0] + 1 < prec
    assert -prec < d[1] < prec
    d = f(3.14159)
    prec = 1e-5
    assert -prec < d[0] + 1 < prec
    assert -prec < d[1] < prec


def test_trig():
    assert theq(aesara_code_(sy.sin(x)), aet.sin(xt))
    assert theq(aesara_code_(sy.tan(x)), aet.tan(xt))


def test_trig():
    assert theq(theano_code_(sy.sin(x)), tt.sin(xt))
    assert theq(theano_code_(sy.tan(x)), tt.tan(xt))

