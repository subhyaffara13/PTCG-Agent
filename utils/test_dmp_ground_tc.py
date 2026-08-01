
def test_dmp_ground_TC():
    assert dmp_ground_TC([[]], 1, ZZ) == 0
    assert dmp_ground_TC([[2, 3, 4], [5]], 1, ZZ) == 5
    assert dmp_ground_TC([[[]]], 2, ZZ) == 0
    assert dmp_ground_TC([[[2], [3, 4]], [[5]]], 2, ZZ) == 5

