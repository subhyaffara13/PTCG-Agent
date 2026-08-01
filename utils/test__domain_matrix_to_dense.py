
def test_DomainMatrix_to_dense():
    A = DomainMatrix({0: {0: 1, 1: 2}, 1: {0: 3, 1: 4}}, (2, 2), ZZ)
    A_dense = A.to_dense()
    ddm = DDM([[1, 2], [3, 4]], (2, 2), ZZ)
    if GROUND_TYPES != 'flint':
        assert A_dense.rep == ddm
    else:
        assert A_dense.rep == ddm.to_dfm()

