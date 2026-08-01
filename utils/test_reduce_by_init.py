
def test_reduce_by_init():
    assert reduceby(iseven, add, [1, 2, 3, 4]) == {True: 2 + 4, False: 1 + 3}
    assert reduceby(iseven, add, [1, 2, 3, 4], no_default2) == {True: 2 + 4,
                                                                False: 1 + 3}

