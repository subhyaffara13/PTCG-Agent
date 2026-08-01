
def test_transpose():
    M = Matrix([[1, 2, 3, 4, 5, 6, 7, 8, 9, 0],
                [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]])
    assert M.T == Matrix( [ [1, 1],
                            [2, 2],
                            [3, 3],
                            [4, 4],
                            [5, 5],
                            [6, 6],
                            [7, 7],
                            [8, 8],
                            [9, 9],
                            [0, 0] ])
    assert M.T.T == M
    assert M.T == M.transpose()


def test_transpose():
    M = Matrix([[1, 2, 3, 4, 5, 6, 7, 8, 9, 0],
                [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]])
    assert M.T == Matrix( [ [1, 1],
                            [2, 2],
                            [3, 3],
                            [4, 4],
                            [5, 5],
                            [6, 6],
                            [7, 7],
                            [8, 8],
                            [9, 9],
                            [0, 0] ])
    assert M.T.T == M
    assert M.T == M.transpose()


def test_transpose():
    assert SparseMatrix(((1, 2), (3, 4))).transpose() == \
        SparseMatrix(((1, 3), (2, 4)))


def test_transpose():
    assert transpose(A*B) == Transpose(B)*Transpose(A)
    assert transpose(2*A*B) == 2*Transpose(B)*Transpose(A)
    assert transpose(2*I*C) == 2*I*Transpose(C)

    M = Matrix(2, 2, [1, 2 + I, 3, 4])
    MT = Matrix(2, 2, [1, 3, 2 + I, 4])
    assert transpose(M) == MT
    assert transpose(2*M) == 2*MT
    assert transpose(x*M) == x*MT
    assert transpose(MatMul(2, M)) == MatMul(2, MT).doit()


def test_transpose():
    Sq = MatrixSymbol('Sq', n, n)

    assert transpose(A) == Transpose(A)
    assert Transpose(A).shape == (m, n)
    assert Transpose(A*B).shape == (l, n)
    assert transpose(Transpose(A)) == A
    assert isinstance(Transpose(Transpose(A)), Transpose)

    assert adjoint(Transpose(A)) == Adjoint(Transpose(A))
    assert conjugate(Transpose(A)) == Adjoint(A)

    assert Transpose(eye(3)).doit() == eye(3)

    assert Transpose(S(5)).doit() == S(5)

    assert Transpose(Matrix([[1, 2], [3, 4]])).doit() == Matrix([[1, 3], [2, 4]])

    assert transpose(trace(Sq)) == trace(Sq)
    assert trace(Transpose(Sq)) == trace(Sq)

    assert Transpose(Sq)[0, 1] == Sq[1, 0]

    assert Transpose(A*B).doit() == Transpose(B) * Transpose(A)


def test_transpose():
    a = Symbol('a', complex=True)
    assert transpose(a) == a
    assert transpose(I*a) == I*a

    x, y = symbols('x y')
    assert transpose(transpose(x)) == x
    assert transpose(x + y) == x + y
    assert transpose(x - y) == x - y
    assert transpose(x * y) == x * y
    assert transpose(x / y) == x / y
    assert transpose(-x) == -x

    x, y = symbols('x y', commutative=False)
    assert transpose(transpose(x)) == x
    assert transpose(x + y) == transpose(x) + transpose(y)
    assert transpose(x - y) == transpose(x) - transpose(y)
    assert transpose(x * y) == transpose(y) * transpose(x)
    assert transpose(x / y) == 1 / transpose(y) * transpose(x)
    assert transpose(-x) == -transpose(x)


def test_transpose():
    assert transpose(A).is_commutative is False
    assert transpose(A*A) == transpose(A)**2
    assert transpose(A*B) == transpose(B)*transpose(A)
    assert transpose(A*B**2) == transpose(B)**2*transpose(A)
    assert transpose(A*B - B*A) == \
        transpose(B)*transpose(A) - transpose(A)*transpose(B)
    assert transpose(A + I*B) == transpose(A) + I*transpose(B)

    assert transpose(X) == conjugate(X)
    assert transpose(-I*X) == -I*conjugate(X)
    assert transpose(Y) == -conjugate(Y)
    assert transpose(-I*Y) == I*conjugate(Y)


def test_transpose():
    arr1d = coo_array([1, 0, 3]).T
    assert arr1d.shape == (3,)
    assert_equal(arr1d.toarray(), np.array([1, 0, 3]))

    arr2d = coo_array([[1, 2, 0], [0, 0, 3]])
    assert arr2d.T.shape == (3, 2)
    desired = np.array([[1, 0], [2, 0], [0, 3]])
    assert_equal(arr2d.T.toarray(), desired)
    assert_equal(arr2d.mT.toarray(), desired)
    assert_equal(matrix_transpose(arr2d).toarray(), desired)


def test_transpose(index_or_series_obj):
    obj = index_or_series_obj
    tm.assert_equal(obj.transpose(), obj)


def test_transpose():
    df = DataFrame({"a": [1, 2, 3], "b": 1})
    df_orig = df.copy()
    result = df.transpose()
    assert np.shares_memory(get_array(df, "a"), get_array(result, 0))

    result.iloc[0, 0] = 100
    tm.assert_frame_equal(df, df_orig)

