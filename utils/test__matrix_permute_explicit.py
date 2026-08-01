
def test_MatrixPermute_explicit():
    p = Permutation(0, 1, 2)
    A = MatrixSymbol('A', 3, 3)
    AA = A.as_explicit()
    assert MatrixPermute(A, p, 0).as_explicit() == \
        AA.permute(p, orientation='rows')
    assert MatrixPermute(A, p, 1).as_explicit() == \
        AA.permute(p, orientation='cols')

