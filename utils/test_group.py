
def test_group():
    assert group([]) == []
    assert group([], multiple=False) == []

    assert group([1]) == [[1]]
    assert group([1], multiple=False) == [(1, 1)]

    assert group([1, 1]) == [[1, 1]]
    assert group([1, 1], multiple=False) == [(1, 2)]

    assert group([1, 1, 1]) == [[1, 1, 1]]
    assert group([1, 1, 1], multiple=False) == [(1, 3)]

    assert group([1, 2, 1]) == [[1], [2], [1]]
    assert group([1, 2, 1], multiple=False) == [(1, 1), (2, 1), (1, 1)]

    assert group([1, 1, 2, 2, 2, 1, 3, 3]) == [[1, 1], [2, 2, 2], [1], [3, 3]]
    assert group([1, 1, 2, 2, 2, 1, 3, 3], multiple=False) == [(1, 2),
                 (2, 3), (1, 1), (3, 2)]

