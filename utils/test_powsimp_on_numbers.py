
def test_powsimp_on_numbers():
    assert 2**(Rational(1, 3) - 2) == 2**Rational(1, 3)/4

