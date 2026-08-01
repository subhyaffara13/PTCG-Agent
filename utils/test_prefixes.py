
def test_prefixes():
    assert list(prefixes([])) == []
    assert list(prefixes([1])) == [[1]]
    assert list(prefixes([1, 2])) == [[1], [1, 2]]

    assert list(prefixes([1, 2, 3, 4, 5])) == \
        [[1], [1, 2], [1, 2, 3], [1, 2, 3, 4], [1, 2, 3, 4, 5]]

