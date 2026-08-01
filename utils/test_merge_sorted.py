
def test_merge_sorted():
    assert list(merge_sorted([1, 2, 3], [1, 2, 3])) == [1, 1, 2, 2, 3, 3]
    assert list(merge_sorted([1, 3, 5], [2, 4, 6])) == [1, 2, 3, 4, 5, 6]
    assert list(merge_sorted([1], [2, 4], [3], [])) == [1, 2, 3, 4]
    assert list(merge_sorted([5, 3, 1], [6, 4, 3], [],
                             key=lambda x: -x)) == [6, 5, 4, 3, 3, 1]
    assert list(merge_sorted([2, 1, 3], [1, 2, 3],
                             key=lambda x: x // 3)) == [2, 1, 1, 2, 3, 3]
    assert list(merge_sorted([2, 3], [1, 3],
                             key=lambda x: x // 3)) == [2, 1, 3, 3]
    assert ''.join(merge_sorted('abc', 'abc', 'abc')) == 'aaabbbccc'
    assert ''.join(merge_sorted('abc', 'abc', 'abc', key=ord)) == 'aaabbbccc'
    assert ''.join(merge_sorted('cba', 'cba', 'cba',
                                key=lambda x: -ord(x))) == 'cccbbbaaa'
    assert list(merge_sorted([1], [2, 3, 4], key=identity)) == [1, 2, 3, 4]

    data = [[(1, 2), (0, 4), (3, 6)], [(5, 3), (6, 5), (8, 8)],
            [(9, 1), (9, 8), (9, 9)]]
    assert list(merge_sorted(*data, key=lambda x: x[1])) == [
        (9, 1), (1, 2), (5, 3), (0, 4), (6, 5), (3, 6), (8, 8), (9, 8), (9, 9)]
    assert list(merge_sorted()) == []
    assert list(merge_sorted([1, 2, 3])) == [1, 2, 3]
    assert list(merge_sorted([1, 4, 5], [2, 3])) == [1, 2, 3, 4, 5]
    assert list(merge_sorted([1, 4, 5], [2, 3], key=identity)) == [
        1, 2, 3, 4, 5]
    assert list(merge_sorted([1, 5], [2], [4, 7], [3, 6], key=identity)) == [
        1, 2, 3, 4, 5, 6, 7]

