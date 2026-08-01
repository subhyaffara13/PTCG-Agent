
def test_DomainMatrix_charpoly_factor_list():
    A = DomainMatrix([], (0, 0), ZZ)
    assert A.charpoly_factor_list() == []

    A = DM([[1]], ZZ)
    assert A.charpoly_factor_list() == [
        ([ZZ(1), ZZ(-1)], 1)
    ]

    A = DM([[1, 2], [3, 4]], ZZ)
    assert A.charpoly_factor_list() == [
        ([ZZ(1), ZZ(-5), ZZ(-2)], 1)
    ]

    A = DM([[1, 2, 0], [3, 4, 0], [0, 0, 1]], ZZ)
    assert A.charpoly_factor_list() == [
        ([ZZ(1), ZZ(-1)], 1),
        ([ZZ(1), ZZ(-5), ZZ(-2)], 1)
    ]

