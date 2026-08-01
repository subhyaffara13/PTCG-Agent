
def test_mersenne_prime_exponent():
    assert mersenne_prime_exponent(1) == 2
    assert mersenne_prime_exponent(4) == 7
    assert mersenne_prime_exponent(10) == 89
    assert mersenne_prime_exponent(25) == 21701
    raises(ValueError, lambda: mersenne_prime_exponent(52))
    raises(ValueError, lambda: mersenne_prime_exponent(0))

