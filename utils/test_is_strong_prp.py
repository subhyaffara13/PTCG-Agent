
def test_is_strong_prp():
    # invalid input
    raises(ValueError, lambda: is_strong_prp(0, 10))
    raises(ValueError, lambda: is_strong_prp(5, 1))

    # n = 1
    assert not is_strong_prp(1, 3)

    # n is prime
    assert is_strong_prp(2, 4)
    assert is_strong_prp(3, 2)
    assert is_strong_prp(11, 3)
    assert is_strong_prp(2**31-1, 5)

    # A001262
    pseudorpime = [2047, 3277, 4033, 4681, 8321, 15841, 29341,
                   42799, 49141, 52633, 65281, 74665, 80581]
    for n in pseudorpime:
        assert is_strong_prp(n, 2)

    # A020229
    pseudorpime = [121, 703, 1891, 3281, 8401, 8911, 10585, 12403,
                   16531, 18721, 19345, 23521, 31621, 44287, 47197]
    for n in pseudorpime:
        assert is_strong_prp(n, 3)

