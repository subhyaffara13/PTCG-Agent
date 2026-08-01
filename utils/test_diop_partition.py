
def test_diop_partition():
    for n in [8, 10]:
        for k in range(1, 8):
            for p in partition(n, k):
                assert len(p) == k
    assert list(partition(3, 5)) == []
    assert [list(p) for p in partition(3, 5, 1)] == [
        [0, 0, 0, 0, 3], [0, 0, 0, 1, 2], [0, 0, 1, 1, 1]]
    assert list(partition(0)) == [()]
    assert list(partition(1, 0)) == [()]
    assert [list(i) for i in partition(3)] == [[1, 1, 1], [1, 2], [3]]

