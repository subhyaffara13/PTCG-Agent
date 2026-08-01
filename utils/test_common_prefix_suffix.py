
def test_common_prefix_suffix():
    assert common_prefix([], [1]) == []
    assert common_prefix(list(range(3))) == [0, 1, 2]
    assert common_prefix(list(range(3)), list(range(4))) == [0, 1, 2]
    assert common_prefix([1, 2, 3], [1, 2, 5]) == [1, 2]
    assert common_prefix([1, 2, 3], [1, 3, 5]) == [1]

    assert common_suffix([], [1]) == []
    assert common_suffix(list(range(3))) == [0, 1, 2]
    assert common_suffix(list(range(3)), list(range(3))) == [0, 1, 2]
    assert common_suffix(list(range(3)), list(range(4))) == []
    assert common_suffix([1, 2, 3], [9, 2, 3]) == [2, 3]
    assert common_suffix([1, 2, 3], [9, 7, 3]) == [3]

