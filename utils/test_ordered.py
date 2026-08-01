
def test_ordered():
    assert list(ordered((x, y), hash, default=False)) in [[x, y], [y, x]]
    assert list(ordered((x, y), hash, default=False)) == \
        list(ordered((y, x), hash, default=False))
    assert list(ordered((x, y))) == [x, y]

    seq, keys = [[[1, 2, 1], [0, 3, 1], [1, 1, 3], [2], [1]],
                 (lambda x: len(x), lambda x: sum(x))]
    assert list(ordered(seq, keys, default=False, warn=False)) == \
        [[1], [2], [1, 2, 1], [0, 3, 1], [1, 1, 3]]
    raises(ValueError, lambda:
           list(ordered(seq, keys, default=False, warn=True)))


def test_ordered():
    # Issue 7210 - this had been failing with python2/3 problems
    assert (list(ordered([{1:3, 2:4, 9:10}, {1:3}])) == \
               [{1: 3}, {1: 3, 2: 4, 9: 10}])
    # warnings should not be raised for identical items
    l = [1, 1]
    assert list(ordered(l, warn=True)) == l
    l = [[1], [2], [1]]
    assert list(ordered(l, warn=True)) == [[1], [1], [2]]
    raises(ValueError, lambda: list(ordered(['a', 'ab'], keys=[lambda x: x[0]],
        default=False, warn=True)))

