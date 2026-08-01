
def test_kind():
    assert C.i.kind is VectorKind(NumberKind)
    assert C.j.kind is VectorKind(NumberKind)
    assert C.k.kind is VectorKind(NumberKind)

    assert C.x.kind is NumberKind
    assert C.y.kind is NumberKind
    assert C.z.kind is NumberKind

    assert Mul._kind_dispatcher(NumberKind, VectorKind(NumberKind)) is VectorKind(NumberKind)
    assert Mul(2, C.i).kind is VectorKind(NumberKind)

    v1 = C.x * i + C.z * C.z * j
    v2 = C.x * i + C.y * j + C.z * k
    assert v1.kind is VectorKind(NumberKind)
    assert v2.kind is VectorKind(NumberKind)

    assert (v1 + v2).kind is VectorKind(NumberKind)
    assert Add(v1, v2).kind is VectorKind(NumberKind)
    assert Cross(v1, v2).doit().kind is VectorKind(NumberKind)
    assert VectorAdd(v1, v2).kind is VectorKind(NumberKind)
    assert VectorMul(2, v1).kind is VectorKind(NumberKind)
    assert VectorZero().kind is VectorKind(NumberKind)

    assert v1.projection(v2).kind is VectorKind(NumberKind)
    assert v2.projection(v1).kind is VectorKind(NumberKind)


def test_kind():
    assert Matrix([[1, 2], [3, 4]]).kind == MatrixKind(NumberKind)
    assert Matrix([[0, 0], [0, 0]]).kind == MatrixKind(NumberKind)
    assert Matrix(0, 0, []).kind == MatrixKind(NumberKind)
    assert Matrix([[x]]).kind == MatrixKind(NumberKind)
    assert Matrix([[1, Matrix([[1]])]]).kind == MatrixKind(UndefinedKind)
    assert SparseMatrix([[1]]).kind == MatrixKind(NumberKind)
    assert SparseMatrix([[1, Matrix([[1]])]]).kind == MatrixKind(UndefinedKind)


def test_kind():
    assert Matrix([[1, 2], [3, 4]]).kind == MatrixKind(NumberKind)
    assert Matrix([[0, 0], [0, 0]]).kind == MatrixKind(NumberKind)
    assert Matrix(0, 0, []).kind == MatrixKind(NumberKind)
    assert Matrix([[x]]).kind == MatrixKind(NumberKind)
    assert Matrix([[1, Matrix([[1]])]]).kind == MatrixKind(UndefinedKind)
    assert SparseMatrix([[1]]).kind == MatrixKind(NumberKind)
    assert SparseMatrix([[1, Matrix([[1]])]]).kind == MatrixKind(UndefinedKind)


def test_kind():
    x = Symbol('x')
    assert unchanged(kind, x)

