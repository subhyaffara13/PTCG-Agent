
def test_num_digits():
    # depending on whether one rounds up or down or uses log or log10,
    # one or more of these will fail if you don't check for the off-by
    # one condition
    assert num_digits(2, 2) == 2
    assert num_digits(2**48 - 1, 2) == 48
    assert num_digits(1000, 10) == 4
    assert num_digits(125, 5) == 4
    assert num_digits(100, 16) == 2
    assert num_digits(-1000, 10) == 4
    # if changes are made to the function, this structured test over
    # this range will expose problems
    for base in range(2, 100):
        for e in range(1, 100):
            n = base**e
            assert num_digits(n, base) == e + 1
            assert num_digits(n + 1, base) == e + 1
            assert num_digits(n - 1, base) == e

