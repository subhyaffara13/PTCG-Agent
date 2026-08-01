
def test_W5():
    # integral is not  calculated
    assert integrate(sqrt(x + 1/x - 2), (x, 0, 2)) == -2*sqrt(2)/3 + R(8, 3)

