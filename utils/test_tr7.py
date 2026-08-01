
def test_TR7():
    assert TR7(cos(x)**2) == cos(2*x)/2 + S.Half
    assert TR7(cos(x)**2 + 1) == cos(2*x)/2 + Rational(3, 2)

