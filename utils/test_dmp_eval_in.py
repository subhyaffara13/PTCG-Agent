
def test_dmp_eval_in():
    assert dmp_eval_in(
        f_6, -2, 1, 3, ZZ) == dmp_eval(dmp_swap(f_6, 0, 1, 3, ZZ), -2, 3, ZZ)
    assert dmp_eval_in(
        f_6, 7, 1, 3, ZZ) == dmp_eval(dmp_swap(f_6, 0, 1, 3, ZZ), 7, 3, ZZ)
    assert dmp_eval_in(f_6, -2, 2, 3, ZZ) == dmp_swap(
        dmp_eval(dmp_swap(f_6, 0, 2, 3, ZZ), -2, 3, ZZ), 0, 1, 2, ZZ)
    assert dmp_eval_in(f_6, 7, 2, 3, ZZ) == dmp_swap(
        dmp_eval(dmp_swap(f_6, 0, 2, 3, ZZ), 7, 3, ZZ), 0, 1, 2, ZZ)

    f = [[[int(45)]], [[]], [[]], [[int(-9)], [-1], [], [int(3), int(0), int(10), int(0)]]]

    assert dmp_eval_in(f, -2, 2, 2, ZZ) == \
        [[45], [], [], [-9, -1, 0, -44]]

    raises(IndexError, lambda: dmp_eval_in(f_6, ZZ(1), -1, 3, ZZ))
    raises(IndexError, lambda: dmp_eval_in(f_6, ZZ(1), 4, 3, ZZ))

