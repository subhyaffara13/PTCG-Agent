
def test_dmp_compose():
    assert dmp_compose([1, 2, 1], [1, 2, 1], 0, ZZ) == [1, 4, 8, 8, 4]

    assert dmp_compose([[[]]], [[[]]], 2, ZZ) == [[[]]]
    assert dmp_compose([[[]]], [[[1]]], 2, ZZ) == [[[]]]
    assert dmp_compose([[[]]], [[[1]], [[2]]], 2, ZZ) == [[[]]]

    assert dmp_compose([[[1]]], [], 2, ZZ) == [[[1]]]

    assert dmp_compose([[1], [2], [ ]], [[]], 1, ZZ) == [[]]
    assert dmp_compose([[1], [2], [1]], [[]], 1, ZZ) == [[1]]

    assert dmp_compose([[1], [2], [1]], [[1]], 1, ZZ) == [[4]]
    assert dmp_compose([[1], [2], [1]], [[7]], 1, ZZ) == [[64]]

    assert dmp_compose([[1], [2], [1]], [[1], [-1]], 1, ZZ) == [[1], [ ], [ ]]
    assert dmp_compose([[1], [2], [1]], [[1], [ 1]], 1, ZZ) == [[1], [4], [4]]

    assert dmp_compose(
        [[1], [2], [1]], [[1], [2], [1]], 1, ZZ) == [[1], [4], [8], [8], [4]]

