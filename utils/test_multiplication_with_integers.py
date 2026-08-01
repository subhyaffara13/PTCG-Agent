
def test_multiplication_with_integers():
    w = omega
    assert 3*w == w
    assert w*9 == Ordinal(OmegaPower(1, 9))

