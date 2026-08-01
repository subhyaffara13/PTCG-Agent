
def test_log_expand():
    w = Symbol("w", positive=True)
    e = log(w**(log(5)/log(3)))
    assert e.expand() == log(5)/log(3) * log(w)
    x, y, z = symbols('x,y,z', positive=True)
    assert log(x*(y + z)).expand(mul=False) == log(x) + log(y + z)
    assert log(log(x**2)*log(y*z)).expand() in [log(2*log(x)*log(y) +
        2*log(x)*log(z)), log(log(x)*log(z) + log(y)*log(x)) + log(2),
        log((log(y) + log(z))*log(x)) + log(2)]
    assert log(x**log(x**2)).expand(deep=False) == log(x)*log(x**2)
    assert log(x**log(x**2)).expand() == 2*log(x)**2
    x, y = symbols('x,y')
    assert log(x*y).expand(force=True) == log(x) + log(y)
    assert log(x**y).expand(force=True) == y*log(x)
    assert log(exp(x)).expand(force=True) == x

    # there's generally no need to expand out logs since this requires
    # factoring and if simplification is sought, it's cheaper to put
    # logs together than it is to take them apart.
    assert log(2*3**2).expand() != 2*log(3) + log(2)

