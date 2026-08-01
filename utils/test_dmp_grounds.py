
def test_dmp_grounds():
    assert dmp_grounds(ZZ(7), 0, 2) == []

    assert dmp_grounds(ZZ(7), 1, 2) == [[[[7]]]]
    assert dmp_grounds(ZZ(7), 2, 2) == [[[[7]]], [[[7]]]]
    assert dmp_grounds(ZZ(7), 3, 2) == [[[[7]]], [[[7]]], [[[7]]]]

    assert dmp_grounds(ZZ(7), 3, -1) == [7, 7, 7]

