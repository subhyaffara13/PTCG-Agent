
def test_exp_expand():
    e = exp(log(Rational(2))*(1 + x) - log(Rational(2))*x)
    assert e.expand() == 2
    assert exp(x + y) != exp(x)*exp(y)
    assert exp(x + y).expand() == exp(x)*exp(y)

