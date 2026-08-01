
def test_block_index_symbolic_fail():
    # To make this work, symbolic matrix dimensions would need to be somehow assumed nonnegative
    # even if the symbols aren't specified as such.  Then 2 * n < n would correctly evaluate to
    # False in BlockMatrix._entry()
    A1 = MatrixSymbol('A1', n, 1)
    A2 = MatrixSymbol('A2', m, 1)
    A = BlockMatrix([[A1], [A2]])
    assert A[2 * n, 0] == A2[n, 0]

