
def test_is_selfridge_prp():
    # invalid input
    raises(ValueError, lambda: is_selfridge_prp(0))

    # n = 1
    assert not is_selfridge_prp(1)

    # n is prime
    assert is_selfridge_prp(2)
    assert is_selfridge_prp(3)
    assert is_selfridge_prp(11)
    assert is_selfridge_prp(2**31-1)

    # A217120
    pseudorpime = [323, 377, 1159, 1829, 3827, 5459, 5777, 9071,
                   9179, 10877, 11419, 11663, 13919, 14839, 16109]
    for n in pseudorpime:
        assert is_selfridge_prp(n)

