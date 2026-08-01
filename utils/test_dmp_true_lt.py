
def test_dmp_true_LT():
    assert dmp_true_LT([[]], 1, ZZ) == ((0, 0), 0)
    assert dmp_true_LT([[7]], 1, ZZ) == ((0, 0), 7)

    assert dmp_true_LT([[1, 0]], 1, ZZ) == ((0, 1), 1)
    assert dmp_true_LT([[1], []], 1, ZZ) == ((1, 0), 1)
    assert dmp_true_LT([[1, 0], []], 1, ZZ) == ((1, 1), 1)

