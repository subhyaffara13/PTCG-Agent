
def test_DomainMatrix_from_Matrix():
    sdm = SDM({0: {0: ZZ(1), 1: ZZ(2)}, 1: {0: ZZ(3), 1: ZZ(4)}}, (2, 2), ZZ)
    A = DomainMatrix.from_Matrix(Matrix([[1, 2], [3, 4]]))
    assert A.rep == sdm
    assert A.shape == (2, 2)
    assert A.domain == ZZ

    K = QQ.algebraic_field(sqrt(2))
    sdm = SDM(
        {0: {0: K.convert(1 + sqrt(2)), 1: K.convert(2 + sqrt(2))},
         1: {0: K.convert(3 + sqrt(2)), 1: K.convert(4 + sqrt(2))}},
        (2, 2),
        K
    )
    A = DomainMatrix.from_Matrix(
        Matrix([[1 + sqrt(2), 2 + sqrt(2)], [3 + sqrt(2), 4 + sqrt(2)]]),
        extension=True)
    assert A.rep == sdm
    assert A.shape == (2, 2)
    assert A.domain == K

    A = DomainMatrix.from_Matrix(Matrix([[QQ(1, 2), QQ(3, 4)], [QQ(0, 1), QQ(0, 1)]]), fmt='dense')
    ddm = DDM([[QQ(1, 2), QQ(3, 4)], [QQ(0, 1), QQ(0, 1)]], (2, 2), QQ)

    if GROUND_TYPES != 'flint':
        assert A.rep == ddm
    else:
        assert A.rep == ddm.to_dfm()
    assert A.shape == (2, 2)
    assert A.domain == QQ

