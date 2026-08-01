
def test_combine_removed():

    assert _combine_removed(6, [0, 1, 2], [0, 1, 2]) == [0, 1, 2, 3, 4, 5]
    assert _combine_removed(8, [2, 5], [1, 3, 4]) == [1, 2, 4, 5, 6]
    assert _combine_removed(8, [7], []) == [7]

