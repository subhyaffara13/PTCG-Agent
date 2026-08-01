
def test_is_strong_selfridge_prp():
    # invalid input
    raises(ValueError, lambda: is_strong_selfridge_prp(0))

    # n = 1
    assert not is_strong_selfridge_prp(1)

    # n is prime
    assert is_strong_selfridge_prp(2)
    assert is_strong_selfridge_prp(3)
    assert is_strong_selfridge_prp(11)
    assert is_strong_selfridge_prp(2**31-1)

    # A217255
    pseudorpime = [5459, 5777, 10877, 16109, 18971, 22499, 24569,
                   25199, 40309, 58519, 75077, 97439, 100127, 113573]
    for n in pseudorpime:
        assert is_strong_selfridge_prp(n)

