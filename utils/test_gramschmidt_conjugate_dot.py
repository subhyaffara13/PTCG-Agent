
def test_gramschmidt_conjugate_dot():
    vecs = [Matrix([1, I]), Matrix([1, -I])]
    assert Matrix.orthogonalize(*vecs) == \
        [Matrix([[1], [I]]), Matrix([[1], [-I]])]

    vecs = [Matrix([1, I, 0]), Matrix([I, 0, -I])]
    assert Matrix.orthogonalize(*vecs) == \
        [Matrix([[1], [I], [0]]), Matrix([[I/2], [S(1)/2], [-I]])]

    mat = Matrix([[1, I], [1, -I]])
    Q, R = mat.QRdecomposition()
    assert Q * Q.H == Matrix.eye(2)


def test_gramschmidt_conjugate_dot():
    vecs = [Matrix([1, I]), Matrix([1, -I])]
    assert Matrix.orthogonalize(*vecs) == \
        [Matrix([[1], [I]]), Matrix([[1], [-I]])]

    vecs = [Matrix([1, I, 0]), Matrix([I, 0, -I])]
    assert Matrix.orthogonalize(*vecs) == \
        [Matrix([[1], [I], [0]]), Matrix([[I/2], [S(1)/2], [-I]])]

    mat = Matrix([[1, I], [1, -I]])
    Q, R = mat.QRdecomposition()
    assert Q * Q.H == Matrix.eye(2)

