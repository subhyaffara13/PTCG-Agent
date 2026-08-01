
def test_dmp_raise():
    assert dmp_raise([], 2, 0, ZZ) == [[[]]]
    assert dmp_raise([[1]], 0, 1, ZZ) == [[1]]

    assert dmp_raise([[1, 2, 3], [], [2, 3]], 2, 1, ZZ) == \
        [[[[1]], [[2]], [[3]]], [[[]]], [[[2]], [[3]]]]

