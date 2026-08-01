
def test_as_sum_midpoint1():
    e = Integral(sqrt(x**3 + 1), (x, 2, 10))
    assert e.as_sum(1, method="midpoint") == 8*sqrt(217)
    assert e.as_sum(2, method="midpoint") == 4*sqrt(65) + 12*sqrt(57)
    assert e.as_sum(3, method="midpoint") == 8*sqrt(217)/3 + \
        8*sqrt(3081)/27 + 8*sqrt(52809)/27
    assert e.as_sum(4, method="midpoint") == 2*sqrt(730) + \
        4*sqrt(7) + 4*sqrt(86) + 6*sqrt(14)
    assert abs(e.as_sum(4, method="midpoint").n() - e.n()) < 0.5

    e = Integral(sqrt(x**3 + y**3), (x, 2, 10), (y, 0, 10))
    raises(NotImplementedError, lambda: e.as_sum(4))

