
def test_as_sum_midpoint2():
    e = Integral((x + y)**2, (x, 0, 1))
    n = Symbol('n', positive=True, integer=True)
    assert e.as_sum(1, method="midpoint").expand() == Rational(1, 4) + y + y**2
    assert e.as_sum(2, method="midpoint").expand() == Rational(5, 16) + y + y**2
    assert e.as_sum(3, method="midpoint").expand() == Rational(35, 108) + y + y**2
    assert e.as_sum(4, method="midpoint").expand() == Rational(21, 64) + y + y**2
    assert e.as_sum(n, method="midpoint").expand() == \
        y**2 + y + Rational(1, 3) - 1/(12*n**2)

