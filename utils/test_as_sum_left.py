
def test_as_sum_left():
    e = Integral((x + y)**2, (x, 0, 1))
    assert e.as_sum(1, method="left").expand() == y**2
    assert e.as_sum(2, method="left").expand() == Rational(1, 8) + y/2 + y**2
    assert e.as_sum(3, method="left").expand() == Rational(5, 27) + y*Rational(2, 3) + y**2
    assert e.as_sum(4, method="left").expand() == Rational(7, 32) + y*Rational(3, 4) + y**2
    assert e.as_sum(n, method="left").expand() == \
        y**2 + y + Rational(1, 3) - y/n - 1/(2*n) + 1/(6*n**2)
    assert e.as_sum(10, method="left", evaluate=False).has(Sum)

