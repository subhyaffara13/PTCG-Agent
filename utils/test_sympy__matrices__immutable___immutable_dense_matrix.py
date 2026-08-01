
def test_sympy__matrices__immutable__ImmutableDenseMatrix():
    from sympy.matrices.immutable import ImmutableDenseMatrix
    m = ImmutableDenseMatrix([[1, 2], [3, 4]])
    assert _test_args(m)
    assert _test_args(Basic(*list(m)))
    m = ImmutableDenseMatrix(1, 1, [1])
    assert _test_args(m)
    assert _test_args(Basic(*list(m)))
    m = ImmutableDenseMatrix(2, 2, lambda i, j: 1)
    assert m[0, 0] is S.One
    m = ImmutableDenseMatrix(2, 2, lambda i, j: 1/(1 + i) + 1/(1 + j))
    assert m[1, 1] is S.One  # true div. will give 1.0 if i,j not sympified
    assert _test_args(m)
    assert _test_args(Basic(*list(m)))

