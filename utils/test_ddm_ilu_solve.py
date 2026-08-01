
def test_ddm_ilu_solve():
    # Basic example
    # A = [[QQ(1), QQ(2)], [QQ(3), QQ(4)]]
    U = [[QQ(1), QQ(2)], [QQ(0), QQ(-2)]]
    L = [[QQ(1), QQ(0)], [QQ(3), QQ(1)]]
    swaps = []
    b = DDM([[QQ(1)], [QQ(2)]], (2, 1), QQ)
    x = DDM([[QQ(0)], [QQ(0)]], (2, 1), QQ)
    xexp = DDM([[QQ(0)], [QQ(1, 2)]], (2, 1), QQ)
    ddm_ilu_solve(x, L, U, swaps, b)
    assert x == xexp

    # Example with swaps
    # A = [[QQ(0), QQ(2)], [QQ(3), QQ(4)]]
    U = [[QQ(3), QQ(4)], [QQ(0), QQ(2)]]
    L = [[QQ(1), QQ(0)], [QQ(0), QQ(1)]]
    swaps = [(0, 1)]
    b = DDM([[QQ(1)], [QQ(2)]], (2, 1), QQ)
    x = DDM([[QQ(0)], [QQ(0)]], (2, 1), QQ)
    xexp = DDM([[QQ(0)], [QQ(1, 2)]], (2, 1), QQ)
    ddm_ilu_solve(x, L, U, swaps, b)
    assert x == xexp

    # Overdetermined, consistent
    # A = DDM([[QQ(1), QQ(2)], [QQ(3), QQ(4)], [QQ(5), QQ(6)]], (3, 2), QQ)
    U = [[QQ(1), QQ(2)], [QQ(0), QQ(-2)], [QQ(0), QQ(0)]]
    L = [[QQ(1), QQ(0), QQ(0)], [QQ(3), QQ(1), QQ(0)], [QQ(5), QQ(2), QQ(1)]]
    swaps = []
    b = DDM([[QQ(1)], [QQ(2)], [QQ(3)]], (3, 1), QQ)
    x = DDM([[QQ(0)], [QQ(0)]], (2, 1), QQ)
    xexp = DDM([[QQ(0)], [QQ(1, 2)]], (2, 1), QQ)
    ddm_ilu_solve(x, L, U, swaps, b)
    assert x == xexp

    # Overdetermined, inconsistent
    b = DDM([[QQ(1)], [QQ(2)], [QQ(4)]], (3, 1), QQ)
    raises(DMNonInvertibleMatrixError, lambda: ddm_ilu_solve(x, L, U, swaps, b))

    # Square, noninvertible
    # A = DDM([[QQ(1), QQ(2)], [QQ(1), QQ(2)]], (2, 2), QQ)
    U = [[QQ(1), QQ(2)], [QQ(0), QQ(0)]]
    L = [[QQ(1), QQ(0)], [QQ(1), QQ(1)]]
    swaps = []
    b = DDM([[QQ(1)], [QQ(2)]], (2, 1), QQ)
    raises(DMNonInvertibleMatrixError, lambda: ddm_ilu_solve(x, L, U, swaps, b))

    # Underdetermined
    # A = DDM([[QQ(1), QQ(2)]], (1, 2), QQ)
    U = [[QQ(1), QQ(2)]]
    L = [[QQ(1)]]
    swaps = []
    b = DDM([[QQ(3)]], (1, 1), QQ)
    raises(NotImplementedError, lambda: ddm_ilu_solve(x, L, U, swaps, b))

    # Shape mismatch
    b3 = DDM([[QQ(1)], [QQ(2)], [QQ(3)]], (3, 1), QQ)
    raises(DMShapeError, lambda: ddm_ilu_solve(x, L, U, swaps, b3))

    # Empty shape mismatch
    U = [[QQ(1)]]
    L = [[QQ(1)]]
    swaps = []
    x = [[QQ(1)]]
    b = []
    raises(DMShapeError, lambda: ddm_ilu_solve(x, L, U, swaps, b))

    # Empty system
    U = []
    L = []
    swaps = []
    b = []
    x = []
    ddm_ilu_solve(x, L, U, swaps, b)
    assert x == []

