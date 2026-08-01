
def test_dmp_sub_term():
    assert dmp_sub_term([ZZ(1), ZZ(1), ZZ(1)], ZZ(1), 2, 0, ZZ) == \
        dup_sub_term([ZZ(1), ZZ(1), ZZ(1)], ZZ(1), 2, ZZ)
    assert dmp_sub_term(f_0, [[]], 3, 2, ZZ) == f_0
    assert dmp_sub_term(F_0, [[]], 3, 2, QQ) == F_0

