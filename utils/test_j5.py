
def test_J5():
    assert polygamma(0, R(1, 3)) == -log(3) - sqrt(3)*pi/6 - EulerGamma - log(sqrt(3))

