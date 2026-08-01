
def test_dmp_degree_list():
    assert dmp_degree_list([[[[ ]]]], 3) == (-oo, -oo, -oo, -oo)
    assert dmp_degree_list([[[[1]]]], 3) == ( 0, 0, 0, 0)

    assert dmp_degree_list(f_0, 2) == (2, 2, 2)
    assert dmp_degree_list(f_1, 2) == (3, 3, 3)
    assert dmp_degree_list(f_2, 2) == (5, 3, 3)
    assert dmp_degree_list(f_3, 2) == (5, 4, 7)
    assert dmp_degree_list(f_4, 2) == (9, 12, 8)
    assert dmp_degree_list(f_5, 2) == (3, 3, 3)
    assert dmp_degree_list(f_6, 3) == (4, 4, 6, 3)

