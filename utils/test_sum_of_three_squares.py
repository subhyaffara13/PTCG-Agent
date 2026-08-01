
def test_sum_of_three_squares():
    for i in [0, 1, 2, 34, 123, 34304595905, 34304595905394941, 343045959052344,
              800, 801, 802, 803, 804, 805, 806]:
        a, b, c = sum_of_three_squares(i)
        assert a**2 + b**2 + c**2 == i
        assert a >= 0

    # error
    raises(ValueError, lambda: sum_of_three_squares(-1))

    assert sum_of_three_squares(7) is None
    assert sum_of_three_squares((4**5)*15) is None
    # if there are two zeros, there might be a solution
    # with only one zero, e.g. 25 => (0, 3, 4) or
    # with no zeros, e.g. 49 => (2, 3, 6)
    assert sum_of_three_squares(25) == (0, 0, 5)
    assert sum_of_three_squares(4) == (0, 0, 2)

