
def test_dmp_strip():
    assert dmp_strip([0, 1, 0], 0) == [1, 0]

    assert dmp_strip([[]], 1) == [[]]
    assert dmp_strip([[], []], 1) == [[]]
    assert dmp_strip([[], [], []], 1) == [[]]

    assert dmp_strip([[[]]], 2) == [[[]]]
    assert dmp_strip([[[]], [[]]], 2) == [[[]]]
    assert dmp_strip([[[]], [[]], [[]]], 2) == [[[]]]

    assert dmp_strip([[[1]]], 2) == [[[1]]]
    assert dmp_strip([[[]], [[1]]], 2) == [[[1]]]
    assert dmp_strip([[[]], [[1]], [[]]], 2) == [[[1]], [[]]]

