
def test_dmp_l2_norm_squared():
    assert dmp_l2_norm_squared([[[]]], 2, ZZ) == 0
    assert dmp_l2_norm_squared([[[1]]], 2, ZZ) == 1
    assert dmp_l2_norm_squared(f_0, 2, ZZ) == 111

