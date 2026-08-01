
def test_dup_sub_mul():
    assert dup_sub_mul([ZZ(1), ZZ(2), ZZ(3)], [ZZ(3), ZZ(2), ZZ(1)],
               [ZZ(1), ZZ(2)], ZZ) == [ZZ(-3), ZZ(-7), ZZ(-3), ZZ(1)]
    assert dmp_sub_mul([[ZZ(1), ZZ(2)], [ZZ(3)]], [[ZZ(3)], [ZZ(2), ZZ(1)]],
               [[ZZ(1)], [ZZ(2)]], 1, ZZ) == [[ZZ(-3)], [ZZ(-1), ZZ(-5)], [ZZ(-4), ZZ(1)]]

