
def test_matrices():
    for c in (Matrix, Matrix([1, 2, 3]), SparseMatrix, SparseMatrix([[1, 2], [3, 4]])):
        check(c, deprecated=['_smat', '_mat'])


def test_matrices():
    from sympy.matrices import MutableDenseMatrix, MutableSparseMatrix, \
        ImmutableDenseMatrix, ImmutableSparseMatrix
    A = MutableDenseMatrix(
        [[1, -1, 0, 0],
         [0, 1, -1, 0],
         [0, 0, 1, -1],
         [0, 0, 0, 1]]
    )
    B = MutableSparseMatrix(A)
    C = ImmutableDenseMatrix(A)
    D = ImmutableSparseMatrix(A)

    assert mcode(C) == mcode(A) == \
        "{{1, -1, 0, 0}, " \
        "{0, 1, -1, 0}, " \
        "{0, 0, 1, -1}, " \
        "{0, 0, 0, 1}}"

    assert mcode(D) == mcode(B) == \
        "SparseArray[{" \
        "{1, 1} -> 1, {1, 2} -> -1, {2, 2} -> 1, {2, 3} -> -1, " \
        "{3, 3} -> 1, {3, 4} -> -1, {4, 4} -> 1" \
        "}, {4, 4}]"

    # Trivial cases of matrices
    assert mcode(MutableDenseMatrix(0, 0, [])) == '{}'
    assert mcode(MutableSparseMatrix(0, 0, [])) == 'SparseArray[{}, {0, 0}]'
    assert mcode(MutableDenseMatrix(0, 3, [])) == '{}'
    assert mcode(MutableSparseMatrix(0, 3, [])) == 'SparseArray[{}, {0, 3}]'
    assert mcode(MutableDenseMatrix(3, 0, [])) == '{{}, {}, {}}'
    assert mcode(MutableSparseMatrix(3, 0, [])) == 'SparseArray[{}, {3, 0}]'


def test_matrices():
    M = Matrix(2, 2, lambda i, j: (i + j + 1)*sin((i + j + 1)*x))

    assert integrate(M, x) == Matrix([
        [-cos(x), -cos(2*x)],
        [-cos(2*x), -cos(3*x)],
    ])

