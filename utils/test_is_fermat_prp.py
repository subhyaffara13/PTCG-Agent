
def test_is_fermat_prp():
    # invalid input
    raises(ValueError, lambda: is_fermat_prp(0, 10))
    raises(ValueError, lambda: is_fermat_prp(5, 1))

    # n = 1
    assert not is_fermat_prp(1, 3)

    # n is prime
    assert is_fermat_prp(2, 4)
    assert is_fermat_prp(3, 2)
    assert is_fermat_prp(11, 3)
    assert is_fermat_prp(2**31-1, 5)

    # A001567
    pseudorpime = [341, 561, 645, 1105, 1387, 1729, 1905, 2047,
                   2465, 2701, 2821, 3277, 4033, 4369, 4371, 4681]
    for n in pseudorpime:
        assert is_fermat_prp(n, 2)

    # A020136
    pseudorpime = [15, 85, 91, 341, 435, 451, 561, 645, 703, 1105,
                   1247, 1271, 1387, 1581, 1695, 1729, 1891, 1905]
    for n in pseudorpime:
        assert is_fermat_prp(n, 4)

