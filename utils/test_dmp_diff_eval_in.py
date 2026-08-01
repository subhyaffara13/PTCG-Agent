
def test_dmp_diff_eval_in():
    assert dmp_diff_eval_in(f_6, 2, 7, 1, 3, ZZ) == \
        dmp_eval(dmp_diff(dmp_swap(f_6, 0, 1, 3, ZZ), 2, 3, ZZ), 7, 3, ZZ)

    assert dmp_diff_eval_in(f_6, 2, 7, 0, 3, ZZ) == \
        dmp_eval(dmp_diff(f_6, 2, 3, ZZ), 7, 3, ZZ)

    raises(IndexError, lambda: dmp_diff_eval_in(f_6, 1, ZZ(1), 4, 3, ZZ))

