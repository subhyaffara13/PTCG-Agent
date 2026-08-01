
def test_dmp_TC():
    assert dmp_TC([[]], ZZ) == []
    assert dmp_TC([[2, 3, 4], [5]], ZZ) == [5]
    assert dmp_TC([[[]]], ZZ) == [[]]
    assert dmp_TC([[[2], [3, 4]], [[5]]], ZZ) == [[5]]

