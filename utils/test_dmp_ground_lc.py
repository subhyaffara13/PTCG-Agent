
def test_dmp_ground_LC():
    assert dmp_ground_LC([[]], 1, ZZ) == 0
    assert dmp_ground_LC([[2, 3, 4], [5]], 1, ZZ) == 2
    assert dmp_ground_LC([[[]]], 2, ZZ) == 0
    assert dmp_ground_LC([[[2], [3, 4]], [[5]]], 2, ZZ) == 2

