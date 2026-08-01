
def test_linsolve_immutable():
    A = ImmutableDenseMatrix([[1, 1, 2], [0, 1, 2], [0, 0, 1]])
    B = ImmutableDenseMatrix([2, 1, -1])
    assert linsolve([A, B], (x, y, z)) == FiniteSet((1, 3, -1))

    A = ImmutableDenseMatrix([[1, 1, 7], [1, -1, 3]])
    assert linsolve(A) == FiniteSet((5, 2))

