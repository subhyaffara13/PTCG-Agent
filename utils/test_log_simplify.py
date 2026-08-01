
def test_log_simplify():
    x = Symbol("x", positive=True)
    assert log(x**2).expand() == 2*log(x)
    assert expand_log(log(x**(2 + log(2)))) == (2 + log(2))*log(x)

    z = Symbol('z')
    assert log(sqrt(z)).expand() == log(z)/2
    assert expand_log(log(z**(log(2) - 1))) == (log(2) - 1)*log(z)
    assert log(z**(-1)).expand() != -log(z)
    assert log(z**(x/(x+1))).expand() == x*log(z)/(x + 1)

