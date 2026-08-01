
def test_fps_shift():
    f = x**-5*sin(x)
    assert fps(f, x).truncate() == \
        1/x**4 - 1/(6*x**2) + Rational(1, 120) - x**2/5040 + x**4/362880 + O(x**6)

    f = x**2*atan(x)
    assert fps(f, x, rational=False).truncate() == \
        x**3 - x**5/3 + O(x**6)

    f = cos(sqrt(x))*x
    assert fps(f, x).truncate() == \
        x - x**2/2 + x**3/24 - x**4/720 + x**5/40320 + O(x**6)

    f = x**2*cos(sqrt(x))
    assert fps(f, x).truncate() == \
        x**2 - x**3/2 + x**4/24 - x**5/720 + O(x**6)

