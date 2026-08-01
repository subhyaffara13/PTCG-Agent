
def test_generic_zero_matrix():
    z = GenericZeroMatrix()
    n = symbols('n', integer=True)
    A = MatrixSymbol("A", n, n)

    assert z == z
    assert z != A
    assert A != z

    assert z.is_ZeroMatrix

    raises(TypeError, lambda: z.shape)
    raises(TypeError, lambda: z.rows)
    raises(TypeError, lambda: z.cols)

    assert MatAdd() == z
    assert MatAdd(z, A) == MatAdd(A)
    # Make sure it is hashable
    hash(z)

