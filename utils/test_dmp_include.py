
def test_dmp_include():
    assert dmp_include([1, 2, 3], [], 0, ZZ) == [1, 2, 3]

    assert dmp_include([1, 2, 3], [0], 0, ZZ) == [[1, 2, 3]]
    assert dmp_include([1, 2, 3], [1], 0, ZZ) == [[1], [2], [3]]

    assert dmp_include([1, 2, 3], [0, 1], 0, ZZ) == [[[1, 2, 3]]]
    assert dmp_include([1, 2, 3], [1, 2], 0, ZZ) == [[[1]], [[2]], [[3]]]

