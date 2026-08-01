
def test_W15():
    # integral not calculated
    assert integrate(log(gamma(x))*cos(6*pi*x), (x, 0, 1)) == R(1, 12)

