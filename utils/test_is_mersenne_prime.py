
def test_is_mersenne_prime():
    assert is_mersenne_prime(-3) is False
    assert is_mersenne_prime(3) is True
    assert is_mersenne_prime(10) is False
    assert is_mersenne_prime(127) is True
    assert is_mersenne_prime(511) is False
    assert is_mersenne_prime(131071) is True
    assert is_mersenne_prime(2147483647) is True

