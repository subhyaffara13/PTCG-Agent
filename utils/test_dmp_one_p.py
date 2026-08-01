
def test_dmp_one_p():
    assert dmp_one_p([1], 0, ZZ) is True
    assert dmp_one_p([[1]], 1, ZZ) is True
    assert dmp_one_p([[[1]]], 2, ZZ) is True
    assert dmp_one_p([[[12]]], 2, ZZ) is False

