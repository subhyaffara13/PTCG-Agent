
def test_issue_8891():
    for cls in (MutableDenseMatrix, MutableSparseMatrix,
            ImmutableDenseMatrix, ImmutableSparseMatrix):
        m = cls(2, 2, [x + y, 0, 0, 0])
        res = cse([x + y, m])
        ans = ([(x0, x + y)], [x0, cls([[x0, 0], [0, 0]])])
        assert res == ans
        assert isinstance(res[1][-1], cls)

