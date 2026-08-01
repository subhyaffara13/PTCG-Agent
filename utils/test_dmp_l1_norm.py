
def test_dmp_l1_norm():
    assert dmp_l1_norm([[[]]], 2, ZZ) == 0
    assert dmp_l1_norm([[[1]]], 2, ZZ) == 1

    assert dmp_l1_norm(f_0, 2, ZZ) == 31

