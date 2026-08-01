
def test_dmp_max_norm():
    assert dmp_max_norm([[[]]], 2, ZZ) == 0
    assert dmp_max_norm([[[1]]], 2, ZZ) == 1

    assert dmp_max_norm(f_0, 2, ZZ) == 6

