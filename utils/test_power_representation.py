
def test_power_representation():
    tests = [(1729, 3, 2), (234, 2, 4), (2, 1, 2), (3, 1, 3), (5, 2, 2), (12352, 2, 4),
             (32760, 2, 3)]

    for test in tests:
        n, p, k = test
        f = power_representation(n, p, k)

        while True:
            try:
                l = next(f)
                assert len(l) == k

                chk_sum = 0
                for l_i in l:
                    chk_sum = chk_sum + l_i**p
                assert chk_sum == n

            except StopIteration:
                break

    assert list(power_representation(20, 2, 4, True)) == \
        [(1, 1, 3, 3), (0, 0, 2, 4)]
    raises(ValueError, lambda: list(power_representation(1.2, 2, 2)))
    raises(ValueError, lambda: list(power_representation(2, 0, 2)))
    raises(ValueError, lambda: list(power_representation(2, 2, 0)))
    assert list(power_representation(-1, 2, 2)) == []
    assert list(power_representation(1, 1, 1)) == [(1,)]
    assert list(power_representation(3, 2, 1)) == []
    assert list(power_representation(4, 2, 1)) == [(2,)]
    assert list(power_representation(3**4, 4, 6, zeros=True)) == \
        [(1, 2, 2, 2, 2, 2), (0, 0, 0, 0, 0, 3)]
    assert list(power_representation(3**4, 4, 5, zeros=False)) == []
    assert list(power_representation(-2, 3, 2)) == [(-1, -1)]
    assert list(power_representation(-2, 4, 2)) == []
    assert list(power_representation(0, 3, 2, True)) == [(0, 0)]
    assert list(power_representation(0, 3, 2, False)) == []
    # when we are dealing with squares, do feasibility checks
    assert len(list(power_representation(4**10*(8*10 + 7), 2, 3))) == 0
    # there will be a recursion error if these aren't recognized
    big = 2**30
    for i in [13, 10, 7, 5, 4, 2, 1]:
        assert list(sum_of_powers(big, 2, big - i)) == []

