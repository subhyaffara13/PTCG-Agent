
def test_dmp_negative_p():
    assert dmp_negative_p([[[]]], 2, ZZ) is False
    assert dmp_negative_p([[[1], [2]]], 2, ZZ) is False
    assert dmp_negative_p([[[-1], [2]]], 2, ZZ) is True

