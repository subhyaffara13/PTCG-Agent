
def test_J9():
    assert besselj(0, z).diff(z) == - besselj(1, z)

