
def test_matexpr_indexing():
    A = MatrixSymbol('A', n, m)
    A[1, 2]
    A[l, k]
    A[l + 1, k + 1]
    A = MatrixSymbol('A', 2, 1)
    for i in range(-2, 2):
        for j in range(-1, 1):
            A[i, j]

