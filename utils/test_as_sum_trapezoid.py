
def test_as_sum_trapezoid():
    e = Integral((x + y)**2, (x, 0, 1))
    assert e.as_sum(1, method="trapezoid").expand() == y**2 + y + S.Half
    assert e.as_sum(2, method="trapezoid").expand() == y**2 + y + Rational(3, 8)
    assert e.as_sum(3, method="trapezoid").expand() == y**2 + y + Rational(19, 54)
    assert e.as_sum(4, method="trapezoid").expand() == y**2 + y + Rational(11, 32)
    assert e.as_sum(n, method="trapezoid").expand() == \
        y**2 + y + Rational(1, 3) + 1/(6*n**2)
    assert Integral(sign(x), (x, 0, 1)).as_sum(1, 'trapezoid') == S.Half

