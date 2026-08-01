
def test_BlockMatrix_3x3_symbolic():
    # Only test one of these, instead of all permutations, because it's slow
    rowblocksizes = (n, m, k)
    colblocksizes = (m, k, n)
    K = BlockMatrix([
        [MatrixSymbol('M%s%s' % (rows, cols), rows, cols) for cols in colblocksizes]
        for rows in rowblocksizes
    ])
    collapse = block_collapse(K.I)
    assert isinstance(collapse, BlockMatrix)

