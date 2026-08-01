
def test_acsch_rewrite():
    x = Symbol('x')
    assert acsch(x).rewrite(log) == log(1/x + sqrt(1/x**2 + 1))
    assert acsch(x).rewrite(asinh) == asinh(1/x)
    assert acsch(x).rewrite(atanh) == (sqrt(-x**2)*(-sqrt(-(x**2 + 1)**2)
                                                    *atanh(sqrt(x**2 + 1))/(x**2 + 1)
                                                    + pi/2)/x)

