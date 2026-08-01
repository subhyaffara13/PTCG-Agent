
def test_dmp_multi_deflate():
    assert dmp_multi_deflate(([[]],), 1, ZZ) == \
        ((1, 1), ([[]],))
    assert dmp_multi_deflate(([[]], [[]]), 1, ZZ) == \
        ((1, 1), ([[]], [[]]))

    assert dmp_multi_deflate(([[1]], [[]]), 1, ZZ) == \
        ((1, 1), ([[1]], [[]]))
    assert dmp_multi_deflate(([[1]], [[2]]), 1, ZZ) == \
        ((1, 1), ([[1]], [[2]]))
    assert dmp_multi_deflate(([[1]], [[2, 0]]), 1, ZZ) == \
        ((1, 1), ([[1]], [[2, 0]]))

    assert dmp_multi_deflate(([[2, 0]], [[2, 0]]), 1, ZZ) == \
        ((1, 1), ([[2, 0]], [[2, 0]]))

    assert dmp_multi_deflate(
        ([[2]], [[2, 0, 0]]), 1, ZZ) == ((1, 2), ([[2]], [[2, 0]]))
    assert dmp_multi_deflate(
        ([[2, 0, 0]], [[2, 0, 0]]), 1, ZZ) == ((1, 2), ([[2, 0]], [[2, 0]]))

    assert dmp_multi_deflate(([2, 0, 0], [1, 0, 4, 0, 1]), 0, ZZ) == \
        ((2,), ([2, 0], [1, 4, 1]))

    f = [[1, 0, 0], [], [1, 0], [], [1]]
    g = [[1, 0, 1, 0], [], [1]]

    assert dmp_multi_deflate((f,), 1, ZZ) == \
        ((2, 1), ([[1, 0, 0], [1, 0], [1]],))

    assert dmp_multi_deflate((f, g), 1, ZZ) == \
        ((2, 1), ([[1, 0, 0], [1, 0], [1]],
                  [[1, 0, 1, 0], [1]]))

