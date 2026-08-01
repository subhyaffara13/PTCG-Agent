
def test_is_euler_prp():
    # invalid input
    raises(ValueError, lambda: is_euler_prp(0, 10))
    raises(ValueError, lambda: is_euler_prp(5, 1))

    # n = 1
    assert not is_euler_prp(1, 3)

    # n is prime
    assert is_euler_prp(2, 4)
    assert is_euler_prp(3, 2)
    assert is_euler_prp(11, 3)
    assert is_euler_prp(2**31-1, 5)

    # A047713
    pseudorpime = [561, 1105, 1729, 1905, 2047, 2465, 3277, 4033,
                   4681, 6601, 8321, 8481, 10585, 12801, 15841]
    for n in pseudorpime:
        assert is_euler_prp(n, 2)

    # A048950
    pseudorpime = [121, 703, 1729, 1891, 2821, 3281, 7381, 8401,
                   8911, 10585, 12403, 15457, 15841, 16531, 18721]
    for n in pseudorpime:
        assert is_euler_prp(n, 3)

