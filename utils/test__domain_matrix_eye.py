
def test_DomainMatrix_eye():
    A = DomainMatrix.eye(3, QQ)
    assert A.rep == SDM.eye((3, 3), QQ)
    assert A.shape == (3, 3)
    assert A.domain == QQ

