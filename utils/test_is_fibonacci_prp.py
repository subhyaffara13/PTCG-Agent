
def test_is_fibonacci_prp():
    # invalid input
    raises(ValueError, lambda: is_fibonacci_prp(3, 2, 1))
    raises(ValueError, lambda: is_fibonacci_prp(3, -5, 1))
    raises(ValueError, lambda: is_fibonacci_prp(3, 5, 2))
    raises(ValueError, lambda: is_fibonacci_prp(0, 5, -1))

    # n = 1
    assert not is_fibonacci_prp(1, 3, 1)

    # n is prime
    assert is_fibonacci_prp(2, 5, 1)
    assert is_fibonacci_prp(3, 6, -1)
    assert is_fibonacci_prp(11, 7, 1)
    assert is_fibonacci_prp(2**31-1, 8, -1)

    # A005845
    pseudorpime = [705, 2465, 2737, 3745, 4181, 5777, 6721,
                   10877, 13201, 15251, 24465, 29281, 34561]
    for n in pseudorpime:
        assert is_fibonacci_prp(n, 1, -1)

