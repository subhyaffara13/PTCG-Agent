
def test_lineintegral():
    c = Curve([E**t + 1, E**t - 1], (t, 0, log(2)))
    assert line_integrate(x + y, c, [x, y]) == 3*sqrt(2)

