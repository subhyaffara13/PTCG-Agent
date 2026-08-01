
def test_DomainMatrix_from_list_sympy():
    ddm = DDM([[ZZ(1), ZZ(2)], [ZZ(3), ZZ(4)]], (2, 2), ZZ)
    A = DomainMatrix.from_list_sympy(2, 2, [[1, 2], [3, 4]])
    if GROUND_TYPES != 'flint':
        assert A.rep == ddm
    else:
        assert A.rep == ddm.to_dfm()
    assert A.shape == (2, 2)
    assert A.domain == ZZ

    K = QQ.algebraic_field(sqrt(2))
    ddm = DDM(
        [[K.convert(1 + sqrt(2)), K.convert(2 + sqrt(2))],
         [K.convert(3 + sqrt(2)), K.convert(4 + sqrt(2))]],
        (2, 2),
        K
    )
    A = DomainMatrix.from_list_sympy(
        2, 2, [[1 + sqrt(2), 2 + sqrt(2)], [3 + sqrt(2), 4 + sqrt(2)]],
        extension=True)
    assert A.rep == ddm
    assert A.shape == (2, 2)
    assert A.domain == K

