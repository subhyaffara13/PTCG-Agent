
def test_dmp_ground_p():
    assert dmp_ground_p([], 0, 0) is True
    assert dmp_ground_p([[]], 0, 1) is True
    assert dmp_ground_p([[]], 1, 1) is False

    assert dmp_ground_p([[ZZ(1)]], 1, 1) is True
    assert dmp_ground_p([[[ZZ(2)]]], 2, 2) is True

    assert dmp_ground_p([[[ZZ(2)]]], 3, 2) is False
    assert dmp_ground_p([[[ZZ(3)], []]], 3, 2) is False

    assert dmp_ground_p([], None, 0) is True
    assert dmp_ground_p([[]], None, 1) is True

    assert dmp_ground_p([ZZ(1)], None, 0) is True
    assert dmp_ground_p([[[ZZ(1)]]], None, 2) is True

    assert dmp_ground_p([[[ZZ(3)], []]], None, 2) is False

