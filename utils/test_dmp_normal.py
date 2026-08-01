
def test_dmp_normal():
    assert dmp_normal([[0], [], [0, 2, 1], [0], [11], []], 1, ZZ) == \
        [[ZZ(2), ZZ(1)], [], [ZZ(11)], []]

