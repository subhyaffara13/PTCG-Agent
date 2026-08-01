
def test_log_polylog():
    assert integrate(log(1 - x)/x, (x, 0, 1)) == -pi**2/6
    assert integrate(log(x)*(1 - x)**(-1), (x, 0, 1)) == -pi**2/6

