
def test_dmp_degree():
    assert dmp_degree([[]], 1) is ninf
    assert dmp_degree([[[]]], 2) is ninf

    assert dmp_degree([[1]], 1) == 0
    assert dmp_degree([[2], [1]], 1) == 1

