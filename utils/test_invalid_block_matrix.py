
def test_invalid_block_matrix():
    raises(ValueError, lambda: BlockMatrix([
        [Identity(2), Identity(5)],
    ]))
    raises(ValueError, lambda: BlockMatrix([
        [Identity(n), Identity(m)],
    ]))
    raises(ValueError, lambda: BlockMatrix([
        [ZeroMatrix(n, n), ZeroMatrix(n, n)],
        [ZeroMatrix(n, n - 1), ZeroMatrix(n, n + 1)],
    ]))
    raises(ValueError, lambda: BlockMatrix([
        [ZeroMatrix(n - 1, n), ZeroMatrix(n, n)],
        [ZeroMatrix(n + 1, n), ZeroMatrix(n, n)],
    ]))

