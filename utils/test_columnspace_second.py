
def test_columnspace_second():
    M = Matrix([[ 1,  2,  0,  2,  5],
                [-2, -5,  1, -1, -8],
                [ 0, -3,  3,  4,  1],
                [ 3,  6,  0, -7,  2]])

    # now check the vectors
    basis = M.columnspace()
    assert basis[0] == Matrix([1, -2, 0, 3])
    assert basis[1] == Matrix([2, -5, -3, 6])
    assert basis[2] == Matrix([2, -1, 4, -7])

    #check by columnspace definition
    a, b, c, d, e = symbols('a b c d e')
    X = Matrix([a, b, c, d, e])
    for i in range(len(basis)):
        eq=M*X-basis[i]
        assert len(solve(eq, X)) != 0

    #check if rank-nullity theorem holds
    assert M.rank() == len(basis)
    assert len(M.nullspace()) + len(M.columnspace()) == M.cols

