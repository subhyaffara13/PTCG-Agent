
def test_is_lucas_prp():
    # invalid input
    raises(ValueError, lambda: is_lucas_prp(3, 2, 1))
    raises(ValueError, lambda: is_lucas_prp(0, 5, -1))
    raises(ValueError, lambda: is_lucas_prp(15, 3, 1))

    # n = 1
    assert not is_lucas_prp(1, 3, 1)

    # n is prime
    assert is_lucas_prp(2, 5, 2)
    assert is_lucas_prp(3, 6, -1)
    assert is_lucas_prp(11, 7, 5)
    assert is_lucas_prp(2**31-1, 8, -3)

    # A081264
    pseudorpime = [323, 377, 1891, 3827, 4181, 5777, 6601, 6721,
                   8149, 10877, 11663, 13201, 13981, 15251, 17119]
    for n in pseudorpime:
        assert is_lucas_prp(n, 1, -1)

