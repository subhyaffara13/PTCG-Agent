
def test_dmp_exclude():
    assert dmp_exclude([[[]]], 2, ZZ) == ([], [[[]]], 2)
    assert dmp_exclude([[[7]]], 2, ZZ) == ([], [[[7]]], 2)

    assert dmp_exclude([1, 2, 3], 0, ZZ) == ([], [1, 2, 3], 0)
    assert dmp_exclude([[1], [2, 3]], 1, ZZ) == ([], [[1], [2, 3]], 1)

    assert dmp_exclude([[1, 2, 3]], 1, ZZ) == ([0], [1, 2, 3], 0)
    assert dmp_exclude([[1], [2], [3]], 1, ZZ) == ([1], [1, 2, 3], 0)

    assert dmp_exclude([[[1, 2, 3]]], 2, ZZ) == ([0, 1], [1, 2, 3], 0)
    assert dmp_exclude([[[1]], [[2]], [[3]]], 2, ZZ) == ([1, 2], [1, 2, 3], 0)


def test_DMP_exclude():
    f = [[[[[[[[[[[[[[[[[[[[[[[[[[ZZ(1)]], [[]]]]]]]]]]]]]]]]]]]]]]]]]]
    J = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17,
        18, 19, 20, 21, 22, 24, 25]

    assert DMP(f, ZZ).exclude() == (J, DMP([ZZ(1), ZZ(0)], ZZ))
    assert DMP([[ZZ(1)], [ZZ(1), ZZ(0)]], ZZ).exclude() ==\
            ([], DMP([[ZZ(1)], [ZZ(1), ZZ(0)]], ZZ))

