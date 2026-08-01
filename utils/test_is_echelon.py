
def test_is_echelon():
    zro = zeros_Reductions(3)
    ident = eye_Reductions(3)

    assert zro.is_echelon
    assert ident.is_echelon

    a = ReductionsOnlyMatrix(0, 0, [])
    assert a.is_echelon

    a = ReductionsOnlyMatrix(2, 3, [3, 2, 1, 0, 0, 6])
    assert a.is_echelon

    a = ReductionsOnlyMatrix(2, 3, [0, 0, 6, 3, 2, 1])
    assert not a.is_echelon

    x = Symbol('x')
    a = ReductionsOnlyMatrix(3, 1, [x, 0, 0])
    assert a.is_echelon

    a = ReductionsOnlyMatrix(3, 1, [x, x, 0])
    assert not a.is_echelon

    a = ReductionsOnlyMatrix(3, 3, [0, 0, 0, 1, 2, 3, 0, 0, 0])
    assert not a.is_echelon


def test_is_echelon():
    zro = zeros(3)
    ident = eye(3)

    assert zro.is_echelon
    assert ident.is_echelon

    a = Matrix(0, 0, [])
    assert a.is_echelon

    a = Matrix(2, 3, [3, 2, 1, 0, 0, 6])
    assert a.is_echelon

    a = Matrix(2, 3, [0, 0, 6, 3, 2, 1])
    assert not a.is_echelon

    x = Symbol('x')
    a = Matrix(3, 1, [x, 0, 0])
    assert a.is_echelon

    a = Matrix(3, 1, [x, x, 0])
    assert not a.is_echelon

    a = Matrix(3, 3, [0, 0, 0, 1, 2, 3, 0, 0, 0])
    assert not a.is_echelon

