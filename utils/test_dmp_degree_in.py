
def test_dmp_degree_in():
    assert dmp_degree_in([[[]]], 0, 2) is ninf
    assert dmp_degree_in([[[]]], 1, 2) is ninf
    assert dmp_degree_in([[[]]], 2, 2) is ninf

    assert dmp_degree_in([[[1]]], 0, 2) == 0
    assert dmp_degree_in([[[1]]], 1, 2) == 0
    assert dmp_degree_in([[[1]]], 2, 2) == 0

    assert dmp_degree_in(f_4, 0, 2) == 9
    assert dmp_degree_in(f_4, 1, 2) == 12
    assert dmp_degree_in(f_4, 2, 2) == 8

    assert dmp_degree_in(f_6, 0, 2) == 4
    assert dmp_degree_in(f_6, 1, 2) == 4
    assert dmp_degree_in(f_6, 2, 2) == 6
    assert dmp_degree_in(f_6, 3, 3) == 3

    raises(IndexError, lambda: dmp_degree_in([[1]], -5, 1))

