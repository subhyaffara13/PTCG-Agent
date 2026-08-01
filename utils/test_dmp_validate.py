
def test_dmp_validate():
    assert dmp_validate([]) == ([], 0)
    assert dmp_validate([0, 0, 0, 1, 0]) == ([1, 0], 0)

    assert dmp_validate([[[]]]) == ([[[]]], 2)
    assert dmp_validate([[0], [], [0], [1], [0]]) == ([[1], []], 1)

    raises(ValueError, lambda: dmp_validate([[0], 0, [0], [1], [0]]))

