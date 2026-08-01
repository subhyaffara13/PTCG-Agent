
def test_dup_multi_deflate():
    assert dup_multi_deflate(([2],), ZZ) == (1, ([2],))
    assert dup_multi_deflate(([], []), ZZ) == (1, ([], []))

    assert dup_multi_deflate(([1, 2, 3],), ZZ) == (1, ([1, 2, 3],))
    assert dup_multi_deflate(([1, 0, 2, 0, 3],), ZZ) == (2, ([1, 2, 3],))

    assert dup_multi_deflate(([1, 0, 2, 0, 3], [2, 0, 0]), ZZ) == \
        (2, ([1, 2, 3], [2, 0]))
    assert dup_multi_deflate(([1, 0, 2, 0, 3], [2, 1, 0]), ZZ) == \
        (1, ([1, 0, 2, 0, 3], [2, 1, 0]))

