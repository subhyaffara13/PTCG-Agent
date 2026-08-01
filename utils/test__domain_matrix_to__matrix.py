
def test_DomainMatrix_to_Matrix():
    A = DomainMatrix([[ZZ(1), ZZ(2)], [ZZ(3), ZZ(4)]], (2, 2), ZZ)
    A_Matrix = Matrix([[1, 2], [3, 4]])
    assert A.to_Matrix() == A_Matrix
    assert A.to_sparse().to_Matrix() == A_Matrix
    assert A.convert_to(QQ).to_Matrix() == A_Matrix
    assert A.convert_to(QQ.algebraic_field(sqrt(2))).to_Matrix() == A_Matrix

