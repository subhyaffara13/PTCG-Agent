
def test_W4():
    # integral is not  calculated
    assert integrate(sqrt(x + 1/x - 2), (x, 1, 2)) == -2*sqrt(2)/3 + R(4, 3)

