
def test_dmp_pow():
    assert dmp_pow([[]], 0, 1, ZZ) == [[ZZ(1)]]
    assert dmp_pow([[]], 0, 1, QQ) == [[QQ(1)]]

    assert dmp_pow([[]], 1, 1, ZZ) == [[]]
    assert dmp_pow([[]], 7, 1, ZZ) == [[]]

    assert dmp_pow([[ZZ(1)]], 0, 1, ZZ) == [[ZZ(1)]]
    assert dmp_pow([[ZZ(1)]], 1, 1, ZZ) == [[ZZ(1)]]
    assert dmp_pow([[ZZ(1)]], 7, 1, ZZ) == [[ZZ(1)]]

    assert dmp_pow([[QQ(3, 7)]], 0, 1, QQ) == [[QQ(1, 1)]]
    assert dmp_pow([[QQ(3, 7)]], 1, 1, QQ) == [[QQ(3, 7)]]
    assert dmp_pow([[QQ(3, 7)]], 7, 1, QQ) == [[QQ(2187, 823543)]]

    f = dup_normal([2, 0, 0, 1, 7], ZZ)

    assert dmp_pow(f, 2, 0, ZZ) == dup_pow(f, 2, ZZ)

