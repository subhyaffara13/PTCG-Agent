
def test_DomainMatrix_solve():
    # XXX: Maybe the _solve method should be changed...
    A = DomainMatrix([[QQ(1), QQ(2)], [QQ(2), QQ(4)]], (2, 2), QQ)
    b = DomainMatrix([[QQ(1)], [QQ(2)]], (2, 1), QQ)
    particular = DomainMatrix([[1, 0]], (1, 2), QQ)
    nullspace = DomainMatrix([[-2, 1]], (1, 2), QQ)
    assert A._solve(b) == (particular, nullspace)

    b3 = DomainMatrix([[QQ(1)], [QQ(1)], [QQ(1)]], (3, 1), QQ)
    raises(DMShapeError, lambda: A._solve(b3))

    bz = DomainMatrix([[ZZ(1)], [ZZ(1)]], (2, 1), ZZ)
    raises(DMNotAField, lambda: A._solve(bz))

