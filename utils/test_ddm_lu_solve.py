
def test_DDM_lu_solve():
    # Basic example
    A = DDM([[QQ(1), QQ(2)], [QQ(3), QQ(4)]], (2, 2), QQ)
    b = DDM([[QQ(1)], [QQ(2)]], (2, 1), QQ)
    x = DDM([[QQ(0)], [QQ(1, 2)]], (2, 1), QQ)
    assert A.lu_solve(b) == x

    # Example with swaps
    A = DDM([[QQ(0), QQ(2)], [QQ(3), QQ(4)]], (2, 2), QQ)
    assert A.lu_solve(b) == x

    # Overdetermined, consistent
    A = DDM([[QQ(1), QQ(2)], [QQ(3), QQ(4)], [QQ(5), QQ(6)]], (3, 2), QQ)
    b = DDM([[QQ(1)], [QQ(2)], [QQ(3)]], (3, 1), QQ)
    assert A.lu_solve(b) == x

    # Overdetermined, inconsistent
    b = DDM([[QQ(1)], [QQ(2)], [QQ(4)]], (3, 1), QQ)
    raises(DMNonInvertibleMatrixError, lambda: A.lu_solve(b))

    # Square, noninvertible
    A = DDM([[QQ(1), QQ(2)], [QQ(1), QQ(2)]], (2, 2), QQ)
    b = DDM([[QQ(1)], [QQ(2)]], (2, 1), QQ)
    raises(DMNonInvertibleMatrixError, lambda: A.lu_solve(b))

    # Underdetermined
    A = DDM([[QQ(1), QQ(2)]], (1, 2), QQ)
    b = DDM([[QQ(3)]], (1, 1), QQ)
    raises(NotImplementedError, lambda: A.lu_solve(b))

    # Domain mismatch
    bz = DDM([[ZZ(1)], [ZZ(2)]], (2, 1), ZZ)
    raises(DMDomainError, lambda: A.lu_solve(bz))

    # Shape mismatch
    b3 = DDM([[QQ(1)], [QQ(2)], [QQ(3)]], (3, 1), QQ)
    raises(DMShapeError, lambda: A.lu_solve(b3))

