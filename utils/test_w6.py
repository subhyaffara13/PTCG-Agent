
def test_W6():
    # integral is not  calculated
    assert integrate(sqrt(2 - 2*cos(2*x))/2, (x, pi*R(-3, 4), -pi/4)) == sqrt(2)

