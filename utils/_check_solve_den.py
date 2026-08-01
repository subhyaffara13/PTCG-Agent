
def _check_solve_den(A, b, xnum, xden):
    # Examples for solve_den, solve_den_charpoly, solve_den_rref should use
    # this so that all methods and types are tested.

    case1 = (A, xnum, b)
    case2 = (A.to_sparse(), xnum.to_sparse(), b.to_sparse())

    for Ai, xnum_i, b_i in [case1, case2]:
        # The key invariant for solve_den:
        assert Ai*xnum_i == xden*b_i

        # solve_den_rref can differ at least by a minus sign
        answers = [(xnum_i, xden), (-xnum_i, -xden)]
        assert Ai.solve_den(b) in answers
        assert Ai.solve_den(b, method='rref') in answers
        assert Ai.solve_den_rref(b) in answers

        # charpoly can only be used if A is square and guarantees to return the
        # actual determinant as a denominator.
        m, n = Ai.shape
        if m == n:
            assert Ai.solve_den(b_i, method='charpoly') == (xnum_i, xden)
            assert Ai.solve_den_charpoly(b_i) == (xnum_i, xden)
        else:
            raises(DMNonSquareMatrixError, lambda: Ai.solve_den_charpoly(b))
            raises(DMNonSquareMatrixError, lambda: Ai.solve_den(b, method='charpoly'))

