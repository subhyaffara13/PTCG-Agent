
def test_TRpower():
    assert TRpower(1/sin(x)**2) == 1/sin(x)**2
    assert TRpower(cos(x)**3*sin(x/2)**4) == \
        (3*cos(x)/4 + cos(3*x)/4)*(-cos(x)/2 + cos(2*x)/8 + Rational(3, 8))
    for k in range(2, 8):
        assert verify_numerically(sin(x)**k, TRpower(sin(x)**k))
        assert verify_numerically(cos(x)**k, TRpower(cos(x)**k))

