
def test_dmp_positive_p():
    assert dmp_positive_p([[[]]], 2, ZZ) is False
    assert dmp_positive_p([[[1], [2]]], 2, ZZ) is True
    assert dmp_positive_p([[[-1], [2]]], 2, ZZ) is False

