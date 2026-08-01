
def test_dmp_zero_p():
    assert dmp_zero_p([], 0) is True
    assert dmp_zero_p([[]], 1) is True

    assert dmp_zero_p([[[]]], 2) is True
    assert dmp_zero_p([[[1]]], 2) is False

