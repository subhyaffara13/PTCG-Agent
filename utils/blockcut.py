
def blockcut(expr, rowsizes, colsizes):
    """ Cut a matrix expression into Blocks

    >>> from sympy import ImmutableMatrix, blockcut
    >>> M = ImmutableMatrix(4, 4, range(16))
    >>> B = blockcut(M, (1, 3), (1, 3))
    >>> type(B).__name__
    'BlockMatrix'
    >>> ImmutableMatrix(B.blocks[0, 1])
    Matrix([[1, 2, 3]])
    """

    rowbounds = bounds(rowsizes)
    colbounds = bounds(colsizes)
    return BlockMatrix([[MatrixSlice(expr, rowbound, colbound)
                         for colbound in colbounds]
                         for rowbound in rowbounds])

