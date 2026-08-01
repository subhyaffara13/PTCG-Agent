
def test_DomainMatrix_ones():
    A = DomainMatrix.ones((2, 3), QQ)
    if GROUND_TYPES != 'flint':
        assert A.rep == DDM.ones((2, 3), QQ)
    else:
        assert A.rep == SDM.ones((2, 3), QQ).to_dfm()
    assert A.shape == (2, 3)
    assert A.domain == QQ

