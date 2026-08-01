
def test_prime_composite():
    assert satask(Q.prime(x), Q.composite(x)) is False
    assert satask(Q.composite(x), Q.prime(x)) is False
    assert satask(Q.composite(x), ~Q.prime(x)) is None
    assert satask(Q.prime(x), ~Q.composite(x)) is None
    # since 1 is neither prime nor composite the following should hold
    assert satask(Q.prime(x), Q.integer(x) & Q.positive(x) & ~Q.composite(x)) is None
    assert satask(Q.prime(2)) is True
    assert satask(Q.prime(4)) is False
    assert satask(Q.prime(1)) is False
    assert satask(Q.composite(1)) is False

