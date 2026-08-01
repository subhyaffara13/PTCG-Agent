
def test_dmp_LC():
    assert dmp_LC([[]], ZZ) == []
    assert dmp_LC([[2, 3, 4], [5]], ZZ) == [2, 3, 4]
    assert dmp_LC([[[]]], ZZ) == [[]]
    assert dmp_LC([[[2], [3, 4]], [[5]]], ZZ) == [[2], [3, 4]]

