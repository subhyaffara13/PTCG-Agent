
def test_is_strong_lucas_prp():
    # invalid input
    raises(ValueError, lambda: is_strong_lucas_prp(3, 2, 1))
    raises(ValueError, lambda: is_strong_lucas_prp(0, 5, -1))
    raises(ValueError, lambda: is_strong_lucas_prp(15, 3, 1))

    # n = 1
    assert not is_strong_lucas_prp(1, 3, 1)

    # n is prime
    assert is_strong_lucas_prp(2, 5, 2)
    assert is_strong_lucas_prp(3, 6, -1)
    assert is_strong_lucas_prp(11, 7, 5)
    assert is_strong_lucas_prp(2**31-1, 8, -3)

