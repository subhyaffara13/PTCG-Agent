
def test_is_gaussianprime():
    assert is_gaussian_prime(7*I)
    assert is_gaussian_prime(7)
    assert is_gaussian_prime(2 + 3*I)
    assert not is_gaussian_prime(2 + 2*I)

