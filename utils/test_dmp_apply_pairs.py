
def test_dmp_apply_pairs():
    h = lambda a, b: a*b

    assert dmp_apply_pairs([1, 2, 3], [4, 5, 6], h, [], 0, ZZ) == [4, 10, 18]

    assert dmp_apply_pairs([2, 3], [4, 5, 6], h, [], 0, ZZ) == [10, 18]
    assert dmp_apply_pairs([1, 2, 3], [5, 6], h, [], 0, ZZ) == [10, 18]

    assert dmp_apply_pairs(
        [[1, 2], [3]], [[4, 5], [6]], h, [], 1, ZZ) == [[4, 10], [18]]

    assert dmp_apply_pairs(
        [[1, 2], [3]], [[4], [5, 6]], h, [], 1, ZZ) == [[8], [18]]
    assert dmp_apply_pairs(
        [[1], [2, 3]], [[4, 5], [6]], h, [], 1, ZZ) == [[5], [18]]

