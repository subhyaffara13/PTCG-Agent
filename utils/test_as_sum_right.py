
def test_as_sum_right():
    e = Integral((x + y)**2, (x, 0, 1))
    assert e.as_sum(1, method="right").expand() == 1 + 2*y + y**2
    assert e.as_sum(2, method="right").expand() == Rational(5, 8) + y*Rational(3, 2) + y**2
    assert e.as_sum(3, method="right").expand() == Rational(14, 27) + y*Rational(4, 3) + y**2
    assert e.as_sum(4, method="right").expand() == Rational(15, 32) + y*Rational(5, 4) + y**2
    assert e.as_sum(n, method="right").expand() == \
        y**2 + y + Rational(1, 3) + y/n + 1/(2*n) + 1/(6*n**2)

