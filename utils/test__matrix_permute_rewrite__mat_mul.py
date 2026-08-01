
def test_MatrixPermute_rewrite_MatMul():
    p = Permutation(0, 1, 2)
    A = MatrixSymbol('A', 3, 3)

    assert MatrixPermute(A, p, 0).rewrite(MatMul).as_explicit() == \
        MatrixPermute(A, p, 0).as_explicit()
    assert MatrixPermute(A, p, 1).rewrite(MatMul).as_explicit() == \
        MatrixPermute(A, p, 1).as_explicit()

